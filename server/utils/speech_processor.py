import os
from typing import Tuple

from server.app_config import CONFIG
from server.utils.logger import log


class SpeechProcessor:

    def create_speech_file(self, text: str, file_name: str) -> Tuple[bool, str]:
        pass


class YandexSpeechKitProcessor(SpeechProcessor):

    def create_speech_file(self, text: str, file_name: str) -> Tuple[bool, str]:
        return True, "file_example_MP3_1MG.mp3"


class DummySpeechKitProcessor(SpeechProcessor):

    def create_speech_file(self, text: str, file_name: str) -> Tuple[bool, str]:
        example_file_path = os.path.join(CONFIG.data_folder, "file_example_MP3_1MG.mp3")
        out_file_path = os.path.join(CONFIG.mp3_location, file_name)
        with open(example_file_path, 'rb') as example_file:
            with open(out_file_path, 'wb') as out_file:
                out_file.write(example_file.read())

        return True, out_file_path


__SELECTION_MAP = {
    "Yandex": YandexSpeechKitProcessor,
    "Dummy": DummySpeechKitProcessor
}

CURRENT_PROCESSOR = __SELECTION_MAP[CONFIG.speech_processor]()
log(f"Initialized speech processor : {CONFIG.speech_processor}")
