import datetime
from typing import Optional

from sqlalchemy import (
    String,
    Date,
    DECIMAL,
    Float,
    Text, UniqueConstraint,
)
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
    date: Mapped[datetime.datetime] = mapped_column(Date, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    overview: Mapped[Optional[str]] = mapped_column(Text)
    crew: Mapped[str] = mapped_column(Text, nullable=False)
    orig_title: Mapped[str] = mapped_column(String, nullable=False)
    budget: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    revenue: Mapped[float] = mapped_column(Float, nullable=False)
    country: Mapped[str] = mapped_column(String(3), nullable=False)

    __table_args__ =(
        UniqueConstraint('name', 'date', name='unique_movie_constraint')
    )

    def __repr__(self):
        return f"<Movie #{self.id!r} (title={self.title!r}, release_date={self.date!r}, score={self.score!r})>"
