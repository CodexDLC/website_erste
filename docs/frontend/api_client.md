[🏠 Home](../../index.md) > [Frontend](../index.md)

# 🔌 API Client Strategy

План перехода от прототипа (`localStorage`) к реальному REST API.

## 🔄 Текущее состояние (AS IS)
Данные хранятся в браузере пользователя.
*   **Плюсы:** Работает без бэкенда, мгновенный отклик.
*   **Минусы:** Данные пропадают при очистке кеша, не видны на других устройствах, Base64 забивает память.

**Файл:** `js/storage.js`

```javascript
function getGalleryData() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY));
}
```

## 🚀 Целевое состояние (TO BE)
Данные хранятся на сервере PinLite Backend.

**Новый файл:** `js/api.js` (заменит `storage.js`)

### 1. Аутентификация
*   Использовать `fetch` для отправки POST `/api/v1/auth/login`.
*   Сохранять JWT Access Token (в памяти или Cookie).

### 2. Загрузка файлов
*   Использовать `FormData` для отправки файлов.
*   POST `/api/v1/media/upload`.

```javascript
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/v1/media/upload', {
        method: 'POST',
        body: formData,
        // Headers (Authorization) будут добавлены автоматически или через интерцептор
    });
    return await response.json();
}
```

### 3. Получение галереи
*   GET `/api/v1/media/feed` (или `/users/me/gallery`).

```javascript
async function getGallery() {
    const response = await fetch('/api/v1/media/feed');
    return await response.json();
}
```

## 📅 План миграции (Phase 4)
1.  Создать `js/api.js` с базовыми методами `fetch`.
2.  Реализовать форму входа (`login.html`).
3.  Переписать `upload.js` на использование `api.uploadFile`.
4.  Переписать `images.js` на использование `api.getGallery`.

---
[⬅️ Назад к Frontend](./index.md)
