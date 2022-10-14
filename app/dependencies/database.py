from typing import Generator

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from app.database.database import session_factory


# Dependency Injection for FastApi routers
# https://fastapi.tiangolo.com/tutorial/sql-databases/
def session() -> Generator[Session, None, None]:
    factory = session_factory()
    if factory is None:
        logger.critical("Database was not initialized")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database was not initialized yet",
        )
    _session = factory()
    try:
        yield _session
    except DBAPIError as error:
        logger.error(error)
        _session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed",
        )
    finally:
        logger.debug("Closing session")
        _session.close()
