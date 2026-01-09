[🏠 Home](../../../../index.md) > [Backend](../../../index.md) > [Architecture](../../index.md) > [Domains](../index.md) > [Media](./index.md)

# 🔌 API Layer (Routers)

Ручки (Endpoints) Media домена.

## Endpoints

### `POST /media/upload`
*   **Auth:** Требуется (`Bearer Token`).
*   **Вход:** `Multipart/Form-Data`.
    *   `file`: Бинарные данные.
*   **Действие:** Вызывает `MediaService.upload_image`.
*   **Ответ:** `201 Created` + JSON с ID картинки и ссылками.

### `GET /media/feed`
*   **Auth:** Не требуется (публичный доступ).
*   **Вход:** Query params:
    *   `limit` (default: 20)
    *   `offset` (default: 0)
*   **Действие:** Вызывает `MediaService.get_public_feed`.
*   **Ответ:** `200 OK` + Список "легких" объектов (только миниатюры).

### `GET /media/{image_id}`
*   **Auth:** Не требуется.
*   **Вход:** Path param `image_id` (UUID).
*   **Действие:** Вызывает `MediaService.get_image_details`.
*   **Ответ:** `200 OK` + Полный объект (оригинал + инфо).

### `DELETE /media/{image_id}`
*   **Auth:** Требуется (`Bearer Token`).
*   **Вход:** Path param `image_id` (UUID).
*   **Действие:** Вызывает `MediaService.delete_image`.
*   **Ответ:** `204 No Content`.

---
[🏠 Вернуться на главную](../../../../index.md)
