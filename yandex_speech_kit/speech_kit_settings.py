from pydantic import BaseSettings


class YandexSpeechKitSettings(BaseSettings):
    """
        Specific settings for Yandex API, as a voice and an emotion.
    """
    #  auth
    AM_TOKEN: str = "NOT_SET"
    FOLDER_ID: str
    YANDEX_PASSPORT_TOKEN: str

    # voice settings
    KIT_VOICE: str = "filipp"
    KIT_EMOTION: str = "good"

    TOKEN_RENEWAL_INTERVAL: int = 30 * 60  # 30 minutes

    class Config:
        env_file = ".env"


yandex_settings = YandexSpeechKitSettings()
