# type: ignore
from __future__ import annotations

import sqlalchemy as orm

from sqlalchemy.orm import declarative_base

SqlAlchemyBase = declarative_base()


class Oversize(SqlAlchemyBase):
    __tablename__ = "oversizes"

    id: int = orm.Column(orm.Integer, primary_key=True, autoincrement=True)

    stone_class: int = orm.Column(orm.Integer, nullable=False)
    datetime: str = orm.Column(orm.String, nullable=False)

    def __repr__(self):
        return f"Oversize(id:{str(self.id)})"
