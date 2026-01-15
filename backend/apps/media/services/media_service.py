import hashlib
import shutil
import os
import uuid
from uuid import UUID
from typing import List
from pathlib import Path

import aiofiles
from aiofiles import os as aios
from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool
from loguru import logger

from backend.core.config import settings
from backend.core.exceptions import ValidationException, NotFoundException, PermissionDeniedException
from backend.apps.media.contracts.media_repository import IMediaRepository
from backend.apps.media.schemas.media import ImageRead

class MediaService:
    """
    Business logic for Media Domain.
    Handles file validation, CAS storage, deduplication, and image management.
    """

    def __init__(self, repository: IMediaRepository):
        self.repository = repository
        # Настройки из конфига/класса для удобства тестирования
        self.chunk_size = 64 * 1024  # 64KB
        self.max_upload_size = settings.MAX_UPLOAD_SIZE
        
        # Используем settings.UPLOAD_DIR как корень (Path object)
        self.temp_dir = settings.UPLOAD_DIR / "temp"
        self.storage_dir = settings.UPLOAD_DIR / "storage"
        
        # Создаем папки при старте (синхронно, один раз)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def upload_image(self, user_id: UUID, file: UploadFile) -> ImageRead:
        """
        Main entry point for image upload.
        """
        logger.info(f"Starting upload for user {user_id}, filename={file.filename}")
        
        # 1. Генерируем уникальное имя для временного файла
        temp_filename = f"upload_{uuid.uuid4()}.tmp"
        temp_path = self.temp_dir / temp_filename

        try:
            # 2. Читаем поток, считаем хеш и пишем во временный файл (+ проверка размера)
            file_hash, size_bytes = await self._process_stream_to_temp(file, temp_path)
            logger.debug(f"File processed. Hash={file_hash}, Size={size_bytes}")

            # 3. Проверяем дедупликацию (есть ли такой файл в БД?)
            existing_file = await self.repository.get_file_by_hash(file_hash)

            if existing_file:
                logger.info(f"Deduplication HIT: File {file_hash} already exists.")
                # HIT: Файл уже есть
                # Удаляем временный файл, он нам не нужен
                await self._remove_file(temp_path)
                
                # Создаем только ссылку (Image) для пользователя
                image = await self.repository.create_image(
                    user_id=user_id,
                    file_hash=file_hash,
                    filename=file.filename or "unknown"
                )
                await self.repository.commit()
                return ImageRead.model_validate(image)

            else:
                logger.info(f"Deduplication MISS: New file {file_hash}.")
                # MISS: Новый файл
                # 4. Перемещаем из temp в постоянное хранилище (Atomic Move)
                target_path = self._get_storage_path(file_hash)
                
                # shutil.move не поддерживает Path объекты в старых версиях, но в 3.11+ ок.
                # На всякий случай приводим к str для run_in_threadpool
                await run_in_threadpool(shutil.move, str(temp_path), str(target_path))

                # 5. Создаем записи в БД
                # Сначала регистрируем физический файл
                await self.repository.create_file(
                    hash=file_hash,
                    size_bytes=size_bytes,
                    mime_type=file.content_type or "application/octet-stream",
                    path=str(target_path)
                )
                
                # Затем создаем ссылку для пользователя
                image = await self.repository.create_image(
                    user_id=user_id,
                    file_hash=file_hash,
                    filename=file.filename or "unknown"
                )
                await self.repository.commit()
                return ImageRead.model_validate(image)

        except Exception as e:
            logger.error(f"Upload failed: {e}")
            # Очистка: удаляем временный файл при любой ошибке
            if temp_path.exists():
                await self._remove_file(temp_path)
            raise e

    async def get_feed(self, limit: int = 20, offset: int = 0) -> List[ImageRead]:
        """
        Get public feed of images.
        """
        images = await self.repository.get_public_images(limit=limit, offset=offset)
        return [ImageRead.model_validate(img) for img in images]

    async def get_user_gallery(self, user_id: UUID, limit: int = 20, offset: int = 0) -> List[ImageRead]:
        """
        Get images for a specific user.
        """
        images = await self.repository.get_images_by_user(user_id=user_id, limit=limit, offset=offset)
        return [ImageRead.model_validate(img) for img in images]

    async def delete_image(self, user_id: UUID, image_id: UUID) -> None:
        """
        Delete an image.
        Checks ownership before deletion.
        """
        image = await self.repository.get_image_by_id(image_id)
        if not image:
            raise NotFoundException(detail="Image not found")
        
        if image.user_id != user_id:
            raise PermissionDeniedException(detail="You do not own this image")
            
        await self.repository.delete_image(image_id)
        await self.repository.commit()
        logger.info(f"Image {image_id} deleted by user {user_id}")

    # --- Private Helpers ---

    async def _process_stream_to_temp(self, upload_file: UploadFile, temp_path: Path) -> tuple[str, int]:
        """
        Reads UploadFile stream, calculates SHA256, and writes to temp_path simultaneously.
        Enforces MAX_UPLOAD_SIZE.
        Returns: (hex_hash, size_bytes)
        """
        sha256 = hashlib.sha256()
        size = 0
        
        # Используем str(temp_path) для aiofiles, так как некоторые версии могут не принимать Path
        async with aiofiles.open(temp_path, 'wb') as out_file:
            while True:
                chunk = await upload_file.read(self.chunk_size)
                if not chunk:
                    break
                
                size += len(chunk)
                if size > self.max_upload_size:
                    # Превышен лимит размера
                    raise ValidationException(
                        detail=f"File too large. Max size is {self.max_upload_size} bytes."
                    )

                # Обновляем хеш
                sha256.update(chunk)
                
                # Пишем на диск
                await out_file.write(chunk)
        
        return sha256.hexdigest(), size

    def _get_storage_path(self, file_hash: str) -> Path:
        """
        Generate sharded path: root/storage/a1/b2/a1b2c3d4...
        Creates directories if needed.
        """
        # Шардинг: a1/b2
        shard = self.storage_dir / file_hash[:2] / file_hash[2:4]
        
        # Создаем папку (синхронно, но это быстро и кешируется ОС)
        os.makedirs(shard, exist_ok=True)
        
        return shard / file_hash

    @staticmethod
    async def _remove_file(path: Path):
        """
        Async wrapper for removing file using aiofiles.os
        """
        if path.exists():
            await aios.remove(path)
