from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import config
from app.models.token import AccessTokenData, RefreshTokenData

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: AccessTokenData) -> str:
    to_encode = data.dict(exclude={"exp"})
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_EXPIRE)
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> AccessTokenData | None:
    try:
        return AccessTokenData(
            **jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
        )
    except JWTError:
        return None


def create_refresh_token(data: RefreshTokenData) -> str:
    to_encode = data.dict(exclude={"exp"})
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=config.JWT_REFRESH_EXPIRE)
    return jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_refresh_token(token: str) -> RefreshTokenData | None:
    try:
        return RefreshTokenData(
            **jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
        )
    except JWTError:
        return None


def decode_token_raw(token: str) -> dict | None:
    try:
        return jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
    except JWTError:
        return None
