import os
import time
from typing import Tuple, Callable

from pydub import AudioSegment

from configs.app_config import CONFIG
from server.utils.logger import log, log_error
from server.utils.yandex_speech.json_merger import merge_json_to_text_for_yandex
from server.utils.yandex_speech.yandex_speech_processor import synthesize


class SpeechProcessor:

    def get_json_merger(self) -> Callable:
        pass

    def create_speech_file(self, text: str, file_name: str) -> Tuple[bool, str]:
        pass


class YandexSpeechKitProcessor(SpeechProcessor):

    def get_json_merger(self) -> Callable:
        return merge_json_to_text_for_yandex

    def create_speech_file(self, ssml_text: str, file_name: str) -> Tuple[bool, str]:
        tmp_file_name = f"tmp-{time.time()}{file_name}.raw"
        tmp_file_path = os.path.join(CONFIG.data_folder, tmp_file_name)
        try:
            with open(tmp_file_path, "wb") as tmp_file:
                for audio_content in synthesize(ssml_text):
                    tmp_file.write(audio_content)
            mp3_file_path = os.path.join(CONFIG.mp3_location, file_name)
            AudioSegment.from_file(
                tmp_file_path, channels=1, sample_width=2, frame_rate=48000
            ).export(mp3_file_path, format="mp3")
        finally:
            if os.path.isfile(tmp_file_path):
                os.remove(tmp_file_path)

        return True, mp3_file_path


class DummySpeechKitProcessor(SpeechProcessor):

    def get_json_merger(self) -> Callable:
        return merge_json_to_text_for_yandex

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

CURRENT_PROCESSOR: SpeechProcessor = __SELECTION_MAP[CONFIG.speech_processor]()
log(f"Initialized speech processor : {CONFIG.speech_processor}")
