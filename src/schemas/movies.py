from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MovieBaseSchema(BaseModel):
    title: str
    genre: str
    date: datetime
    score: float
    overview: Optional[str] = None
    crew: str
    orig_title: str
    budget: float
    revenue: float
    country: str


class MovieCreateSchema(MovieBaseSchema):
    pass


class MovieDetailResponseSchema(MovieBaseSchema):
    id: int

    # to avoid validation and convertion errors from ORM object to JSON object
    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
    movies: list[MovieDetailResponseSchema]

    model_config = ConfigDict(from_attributes=True)
