import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    BigInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    """
    Database model for Users.
    Represents a registered user in the system.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Relationships
    # TODO: Uncomment after full refactoring and resolving circular imports
    # refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    # social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    # images = relationship("Image", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class SocialAccount(Base):
    """
    Database model for Social Accounts (OAuth2).
    Links external providers (Google, GitHub) to a User.
    """

    __tablename__ = "social_accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "google"
    provider_id: Mapped[str] = mapped_column(
        String, nullable=False
    )  # e.g., "1234567890" from Google
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "provider", "provider_id", name="uix_social_account_provider_pid"
        ),
    )

    # Relationships
    # TODO: Uncomment after full refactoring
    # user = relationship("User", back_populates="social_accounts")

    def __repr__(self) -> str:
        return f"<SocialAccount(provider={self.provider}, user_id={self.user_id})>"


class RefreshToken(Base):
    """
    Database model for Refresh Tokens.
    Used for JWT token rotation and session management.
    """

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    # TODO: Uncomment after full refactoring
    # user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id})>"
