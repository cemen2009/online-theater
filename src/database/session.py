from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config.settings import get_settings
from database import Base


settings = get_settings()

DATABASE_URL = f"sqlite+aiosqlite:///{settings.PATH_TO_DATABASE}"
ECHO_SQL_QUERIES = settings.ECHO_SQL_QUERIES

print(f"Connecting to database at: {DATABASE_URL}")
print(f"SQL echo enabled: {ECHO_SQL_QUERIES}")

engine = create_async_engine(DATABASE_URL, echo=ECHO_SQL_QUERIES, future=True)
AsyncSQLiteSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, future=True)   # type: ignore


async def init_db() -> None:
    """
    Initialize the database.

    This function creates all the tables defined in the SQLAlchemy ORM models.
    It should be called at the application startup to ensure that the database schema exists.

    :return: None
    """
    async with engine.begin() as conn:

        # async creation of all undefined tables using sync method Base.metadata.create_all
        # using async connection with DB to not stop main async event loop
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close the database connection.

    This function disposes of the database engine, releasing all associated resources.
    It should be called when the application shuts down to properly close the connection pool.

    :return: None
    """
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.

    This function returns an async generator yielding a new database session.
    It ensures that the session is properly closed after use.

    :return: An asynchronous generator yielding an AsyncSession instance.
    :rtype: AsyncSession
    """
    async with AsyncSQLiteSessionLocal() as session:
        # startup
        yield session
        # tier down


@asynccontextmanager
async def get_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session using a context manager.

    This function allows for managing the database session within a `with` statement.
    It ensures that the session is properly initialized and closed after execution

    :return: An asynchronous generator yielding an AsyncSession instance.
    :rtype: AsyncSession
    """
    async with AsyncSQLiteSessionLocal() as session:
        yield session


async def reset_sqlite_database() -> None:
    """
    Reset the SQLite database.

    This function drops all existing tables and recreates them.
    It is useful for testing purpose or when resetting the database is required.

    Warning: This action is irreversible and will delete all stored data.

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
