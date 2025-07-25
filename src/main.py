from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header

from routers import users, movies
from database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    print("app startup: initializing...")
    await init_db()

    yield

    # shutdown code
    print("app shutdown: disposing of the database...")
    await close_db()


app = FastAPI(
    title="Movies app",
    description="A fastapi app for managing movies.",
    lifespan=lifespan,
)

api_version_prefix = "/api/v1"

app.include_router(movies.router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
app.include_router(users.router, prefix=f"{api_version_prefix}/users")

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
