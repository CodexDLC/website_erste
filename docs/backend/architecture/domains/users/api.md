[🏠 Home](../../../../index.md) > [Backend](../../../index.md) > [Architecture](../../index.md) > [Domains](../index.md) > [Users](./index.md)

# 🔌 API Layer (Routers)

Ручки (Endpoints) должны быть максимально тонкими. Их задача — валидация (Pydantic) и передача управления сервису.

## Endpoints

### `POST /auth/register`
*   **Принимает:** `UserCreate` (email, password).
*   **Валидация:** Pydantic (формат email, длина пароля).
*   **Действие:** Вызывает `AuthService.register_user`.
*   **Возвращает:** `201 Created` + `UserResponse`.

### `POST /auth/login`
*   **Принимает:** `UserLogin` (email, password).
*   **Действие:** Вызывает `AuthService.authenticate_user`.
*   **Возвращает:** `200 OK` + `TokenSchema` (access_token, refresh_token).

### `POST /auth/refresh`
*   **Принимает:** `RefreshTokenSchema` (refresh_token).
*   **Действие:** Вызывает `AuthService.refresh_token`.
*   **Возвращает:** `200 OK` + `TokenSchema`.

### `GET /users/me`
*   **Требует:** `Depends(get_current_user)` — авторизация по Bearer токену.
*   **Действие:** Возвращает профиль текущего пользователя.
*   **Возвращает:** `200 OK` + `UserResponse`.

---
[🏠 Вернуться на главную](../../../../index.md)
