from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    bio: Mapped[Optional[str]]
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<User #{self.id!r} (email={self.email!r})>"


class MovieModel(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    genre: Mapped[str] = mapped_column(String(46), index=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Film #{self.id!r} (title={self.title!r}, genre={self.genre!r}, price={self.price!r})>"
