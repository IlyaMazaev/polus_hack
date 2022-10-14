# type: ignore
from __future__ import annotations

import sqlalchemy as orm
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.orm import Mapped, Session, relationship
from sqlalchemy_serializer import SerializerMixin

from app.database.database import SqlAlchemyBase

from datetime import datetime


class Project(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "stones"



    def __repr__(self):
        return f"Project(id:{str(self.id)}, {str(self.name)})"

    @classmethod
    def get_by_id(cls, session: Session, uid: int) -> Project | None:
        return session.query(cls).filter_by(id=uid).first()

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Project | None:
        return session.query(cls).filter_by(name=name).first()

    def update_data(self, update_dict: dict):
        for col_name in self.__table__.columns.keys():
            if col_name in update_dict:
                setattr(self, col_name, update_dict[col_name])
        self.time_updated = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


PydanticProject = sqlalchemy_to_pydantic(Project)
