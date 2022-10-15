# type: ignore
from __future__ import annotations

import sqlalchemy as orm
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.orm import Mapped, Session, relationship
from sqlalchemy_serializer import SerializerMixin

from pydantic import BaseModel, Field

from app.database.database import SqlAlchemyBase


class Stone(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "stones"

    id: int = orm.Column(orm.Integer, primary_key=True, autoincrement=True)
    frame_id: int = orm.Column(orm.Integer, nullable=False)

    bbox: list = orm.Column(orm.ARRAY(orm.String), nullable=False)
    stone_class: int = orm.Column(orm.Integer, nullable=False)

    def __repr__(self):
        return f"Stone(id:{str(self.id)})"

    @classmethod
    def get_by_id(cls, session: Session, stone_id: int) -> Stone | None:
        return session.query(cls).filter_by(id=stone_id).first()

    @classmethod
    def get_by_frame_id(cls, session: Session, frame_id: int) -> Stone | None:
        return session.query(cls).filter_by(frame_id=frame_id).all()

    @classmethod
    def get_by_class(cls, session: Session, stone_class: int) -> list | None:
        return session.query(cls).filter_by(stone_class=stone_class).all()

    @classmethod
    def get_by_frame_and_class(cls, session: Session, frame_id: int, stone_class: int) -> list | None:
        return session.query(cls).filter_by(frame_id=frame_id).filter_by(stone_class=stone_class).all()


PydanticStone = sqlalchemy_to_pydantic(Stone)


class PydanticStone(BaseModel):
    id: int

    frame_id: int
    bbox: list

    stone_class: int

    class Config:
        orm_mode = True
