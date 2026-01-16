# backend/core/security.py
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=30)

    to_encode = {"exp": expire, "sub": str(subject)}
    # jwt.encode returns Any (untyped library), so we cast or assume it's str
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return cast(str, encoded_jwt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # pwd_context.verify returns Any/bool
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    # pwd_context.hash returns Any/str
    return cast(str, pwd_context.hash(password))
