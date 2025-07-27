import os
from pathlib import Path
from typing import ClassVar
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()   # to load environment variables


class Settings(BaseSettings):
    BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent
    PATH_TO_DATABASE: str = str(BASE_DIR / "database" / "source" / "movies.db")
    PATH_TO_MOVIES_CSV: str = str(BASE_DIR / "database" / "seed_data" / "imdb_movies.csv")
    ECHO_SQL_QUERIES: bool = False


class TestingSettings(Settings):
    # PATH_TO_DATABASE: str = str(super().BASE_DIR / "database" / "source" / "movies.db")
    # PATH_TO_DATABASE: str = ":memory:"
    ECHO_SQL_QUERIES: bool = True



def get_settings() -> Settings | TestingSettings:
    """
    Retrieve an application settings based on environment variable.

    This function checks the `ENVIRONMENT` environment variable to determine
    which settings class to use. If 'ENVIRONMENT' is set to `"testing"`,
    it returns an instance of `TestingSettings`. Otherwise, it defaults to `Settings`.

    :return: An instance of the appropriate settings class.
    :rtype: BaseSettings
    """
    environment = os.getenv("ENVIRONMENT", "developing")
    if environment == "testing":
        return TestingSettings()

    return Settings()
