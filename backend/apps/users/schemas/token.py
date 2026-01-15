from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for JWT Token response.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Schema for JWT Token payload.
    """

    sub: str | None = None
    exp: int | None = None


class RefreshTokenRequest(BaseModel):
    """
    Schema for Refresh Token request.
    """

    refresh_token: str
