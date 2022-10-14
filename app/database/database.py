from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import config

SqlAlchemyBase = declarative_base()


def session_factory():
    global __session_factory
    return __session_factory


def global_init():
    global __session_factory

    if __session_factory:
        return

    engine = create_engine(config.DATABASE_URL)
    __session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    import app.database.models

    SqlAlchemyBase.metadata.create_all(engine)


__session_factory = None
