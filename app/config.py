from functools import cached_property, lru_cache

from pydantic import BaseSettings


# BaseSettings class from pydantic provides convenient way to handle environment variables
class Config(BaseSettings):
    class Config:  # Base Settings Config
        keep_untouched = (cached_property,)

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: str = "5432"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE: int
    JWT_REFRESH_EXPIRE: int
    FRONTEND_HOST: str = "http://localhost"

    @cached_property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


# we should cache result to do IO operation (read & load from .env file) only once
@lru_cache
def get_config():
    return Config()  # type: ignore # load from .env file


# export variable
config = get_config()
