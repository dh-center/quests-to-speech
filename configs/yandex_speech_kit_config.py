class YandexConfig:
    _AM_TOKEN = "t1.9euelZqYj4yZzpqMjZecncmPlZWOz-3rnpWax8eLjpnLzsmcnZ3PyI2Zlpnl9PdANlEB-u8_Z2fn3fT3AGVOAfrvP2dn5w.2IawU__uE5rpuFXA7HmR2AqnuWkdJMW6G-MxqstsOLfxkohkrvrVN8tsUIG7rC-EMgqu8yG3X7mKinV6o_4aBQ"
    _FOLDER_ID = "b1gof8ni37m9mdsnkabm"
    _VOICE = "filipp",
    _EMOTION = "good"

    @property
    def am_token(self):
        return YandexConfig._AM_TOKEN

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
