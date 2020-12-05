class YandexConfig:
    _AM_TOKEN = "_AM_TOKEN"
    _FOLDER_ID = "_FOLDER_ID"

    @property
    def am_token(self):
        return YandexConfig._AM_TOKEN

    @property
    def folder_id(self):
        return YandexConfig._FOLDER_ID


YANDEX_CONFIG = YandexConfig()
