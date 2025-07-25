from pydantic import BaseModel, ConfigDict


class FilmBase(BaseModel):
    title: str
    genre: str
    price: float


class FilmCreate(FilmBase):
    pass


class FilmRead(FilmBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
