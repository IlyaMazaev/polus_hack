# type: ignore
from __future__ import annotations

import sqlalchemy as orm
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy.orm import Mapped, Session, relationship
from sqlalchemy_serializer import SerializerMixin

from pydantic import BaseModel, Field

from app.database.database import SqlAlchemyBase


class Frame(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "frame"

    id: int = orm.Column(orm.Integer, primary_key=True, autoincrement=True)
    frame_id: int = orm.Column(orm.Integer, nullable=False)

    classes: list = orm.Column(orm.ARRAY(orm.String), nullable=False)

    def __repr__(self):
        return f"Frame(id:{str(self.id)})"

    @classmethod
    def get_by_id(cls, session: Session, stone_id: int) -> Frame | None:
        return session.query(cls).filter_by(id=stone_id).first()

    @classmethod
    def get_by_frame_id(cls, session: Session, frame_id: int) -> Frame | None:
        return session.query(cls).filter_by(frame_id=frame_id).all()


PydanticFrame = sqlalchemy_to_pydantic(Frame)


class PydanticFrame(BaseModel):
    id: int

    frame_id: int
    classes: list

    class Config:
        orm_mode = True
