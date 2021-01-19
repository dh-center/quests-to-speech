import os

from pydantic import BaseSettings

DATA_FOLDER_DEFAULT = "data-folder"


class Settings(BaseSettings):
    """
    App settings configuration class (based on .env file).
    """
    DATA_FOLDER: str = DATA_FOLDER_DEFAULT
    # where mp3 files will be kept
    MP3_LOCATION: str = os.path.join(DATA_FOLDER_DEFAULT, "mp3")
    # max text length for a request
    TEXT_LENGTH_LIMIT: int = 500
    # file separator
    FILE_PARTS_SEPARATOR: str = r'$$'

    class Config:
        env_file = ".env"


APP_SETTINGS = Settings()
