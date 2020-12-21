import os


class YandexConfig:
    #  auth
    _AM_TOKEN = os.environ.get('YANDEX_API_AM_TOKEN', '')
    _FOLDER_ID = os.environ.get('YANDEX_API_FOLDER_ID', '')
    _yandexPassportOauthToken = os.environ.get('YANDEX_API_PASSPORT_TOKEN', '')

    # voice settings
    _VOICE = "filipp",
    _EMOTION = "good"

    TOKEN_RENEWAL_INTERVAL = 30 * 60  # 30 minutes

    @property
    def am_token(self):
        return YandexConfig._AM_TOKEN

    @staticmethod
    def set_am_token(token):
        YandexConfig._AM_TOKEN = token

    @property
    def folder_id(self):
        return YandexConfig._FOLDER_ID

    @staticmethod
    def set_folder_id(foldr_id):
        YandexConfig._FOLDER_ID = foldr_id

    @property
    def passport_token(self):
        return YandexConfig._yandexPassportOauthToken

    @staticmethod
    def set_passport_token(passport_token):
        YandexConfig._yandexPassportOauthToken = passport_token

    @property
    def voice(self):
        return YandexConfig._VOICE

    @property
    def emotion(self):
        return YandexConfig._EMOTION


YANDEX_CONFIG = YandexConfig()
