from pydantic import BaseModel, EmailStr


class AccessTokenData(BaseModel):
    email: str


class RefreshTokenData(BaseModel):
    email: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type = "Bearer"


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    patronymic: str | None
    birthday: str | None
    photo_address: str | None
    key_skills: str | None
    useful_to_project: str | None
    status: str | None
    city: str | None
    region: str | None
    organisation: str | None
    achievements: str | None
    tags: str | None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokens(BaseModel):
    refresh_token: str
