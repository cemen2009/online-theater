from typing import Annotated

from fastapi import FastAPI, Header

from routers import users, movies


app = FastAPI()


app.include_router(users.router)
app.include_router(movies.router)

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
