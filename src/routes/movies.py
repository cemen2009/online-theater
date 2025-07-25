from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from schemas import MovieCreateSchema, MovieDetailResponseSchema
from database.models import MovieModel


router = APIRouter()


@router.get('/movies/{film_id}', response_model=MovieDetailResponseSchema)
async def get_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == film_id))
    film = result.scalar_one_or_none()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    return film

@router.post('/movies/', response_model=MovieDetailResponseSchema)
async def create_film(film: MovieCreateSchema, db: AsyncSession = Depends(get_db)):
    new_film = MovieModel(**film.model_dump())
    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)

    return new_film
