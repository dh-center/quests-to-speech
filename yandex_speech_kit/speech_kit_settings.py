from pydantic import BaseSettings


"""
    Our specific settings for api, as a voice and an emotion.
"""
class YandexSpeechKitSettings(BaseSettings):
    #  auth
    am_token: str = "NOT_SET"
    folder_id: str
    yandex_passport_token: str

    # voice settings
    kit_voice: str = "filipp"
    kit_emotion: str = "good"

    token_renewal_interval: int = 30 * 60  # 30 minutes

    class Config:
        env_file = ".env"


yandex_settings = YandexSpeechKitSettings()
