from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header

from routers import users, movies
from database import engine
from database.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app startup: initializing...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # before yield you can put startup code
    yield
    # after yield you can put shutdown code


app = FastAPI(lifespan=lifespan)


app.include_router(users.router)
app.include_router(movies.router)

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
