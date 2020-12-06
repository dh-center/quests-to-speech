class YandexConfig:
    _AM_TOKEN = "t1.9euelZqOmJ7Mlp3Jm5rHk56PkZGViu3rnpWax8eLjpnLzsmcnZ3PyI2Zlpnl8_dNPksB-u8_QBY2_t3z9w1tSAH67z9AFjb-.biw-uouvfcZOMUHZ5AZDSF2-mo4eNF_wCnsS1t4AZG0SnBzAxeSUcjWQvEJXYevDnUY-NeVjcsI11AV8Hp1ZBw"
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
