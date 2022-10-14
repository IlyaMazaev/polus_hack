from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.crypto import decode_access_token, verify_password
from app.database.models.user import UserNativeAuth
from app.dependencies import database

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(session: Session, email: str, password: str) -> bool:
    user = UserNativeAuth.get_by_email(session, email)
    if user is None:
        return False

    return verify_password(password, user.hashed_password)


async def get_current_user(
    token=Depends(oauth_scheme),
    session=Depends(database.session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user = UserNativeAuth.get_by_email(session, payload.email)
    if user is None:
        raise credentials_exception
    return user
