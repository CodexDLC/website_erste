[🏠 Home](../../index.md) > [Management](../index.md) > [Tasks](./index.md)

# 🛡️ Task: Secure Swagger UI

**Status:** 📋 Backlog
**Priority:** High (for Production)
**Related Tech Debt:** Public Swagger

## 📝 Описание проблемы
В данный момент документация API (`/docs` и `/redoc`) и схема OpenAPI (`/openapi.json`) доступны публично.
Это позволяет любому пользователю изучить структуру API, типы данных и эндпоинты, что облегчает поиск уязвимостей злоумышленникам.

## 🎯 Цель
Ограничить доступ к документации API в продакшн-среде.

## 📋 Варианты реализации

### Вариант А: Полное отключение (Простой)
Если `DEBUG=False`, полностью отключаем генерацию документации.

**В `backend/main.py`:**
```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    # ...
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
)
```

### Вариант Б: Basic Auth (Продвинутый)
Оставить доступ к документации, но закрыть её паролем (полезно для QA/Frontend на стейджинге или проде).

1.  Создать зависимость `get_current_username` с использованием `HTTPBasic`.
2.  В `backend/main.py` переопределить роуты документации:

```python
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    # Сравнить credentials.username и credentials.password с переменными окружения
    # SWAGGER_USER / SWAGGER_PASS
    ...

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None) # Отключаем дефолтные

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)
```

## ✅ Критерии приемки
1.  При `DEBUG=True` (локально) Swagger доступен без пароля.
2.  При `DEBUG=False` (продакшн) Swagger либо недоступен (404), либо запрашивает логин/пароль.

---
[⬅️ Вернуться к списку задач](./index.md)
