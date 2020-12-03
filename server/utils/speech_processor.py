from typing import Tuple


class SpeechProcessor:

    def create_speech_file(self, text: str, file_name: str) -> Tuple[bool, str]:
        pass


class YandexSpeechKitProcessor(SpeechProcessor):

    def create_speech_file(self, text: str, file_name: str) -> Tuple[bool, str]:
        return (True, "file_example_MP3_1MG.mp3")


CURRENT_PROCESSOR = YandexSpeechKitProcessor()
