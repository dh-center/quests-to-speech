import os

from pydantic import BaseSettings

DATA_FOLDER = "data-folder"


class Settings(BaseSettings):
    data_folder: str = DATA_FOLDER
    mp3_location: str = os.path.join(DATA_FOLDER, "mp3")
    text_length_limit: int = 500
    file_parts_separator: str = r'$$'

    class Config:
        env_file = ".env"


settings = Settings()
