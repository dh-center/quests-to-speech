class YandexConfig:
    _AM_TOKEN = ""
    _FOLDER_ID = "b1gof8ni37m9mdsnkabm"
    _VOICE = "filipp",
    _EMOTION = "good"

    @property
    def am_token(self):
        return YandexConfig._AM_TOKEN

    @staticmethod
    def set_am_token(token):
        YandexConfig._AM_TOKEN = token

    @property
    def folder_id(self):
        return YandexConfig._FOLDER_ID

    @property
    def voice(self):
        return YandexConfig._VOICE

    @property
    def emotion(self):
        return YandexConfig._EMOTION


YANDEX_CONFIG = YandexConfig()
