import hashlib
import time

from app_source.app_settings import app_settings, Settings
from app_source.logger import main_logger
from yandex_speech_kit.speech_kit import speech_kit_processor, SpeechKit


class AppMethods:
    """
    This class is responsible for serving main needs of controllers for fastapi methods.
    As it has all necessary methods to process file and to check that file is already processed.
    """

    def __init__(self, speech_kit: SpeechKit, settings: Settings):
        self.speech_kit = speech_kit
        self.settings = settings

    @staticmethod
    def hash_text(text: str) -> str:
        """
        Returns sha256 plus length str from given str
        :param text:
        :return: hash based on sha256 of str
        """
        sha = hashlib.sha256()
        sha.update(str.encode(text))
        return f"{sha.hexdigest()}-{len(text)}"

    def route_to_audio_file(self, route_id: str, ssml_text: str, text_hash: str) -> str:
        """
        Given route_id and text's information as text itself and its hash,
        synthesise audio file
        :param ssml_text: content to synthesise audio from
        :param text_hash: hash of content
        :return: file with synthesised audio from provided text
        """
        task_info = f"route_to_audio_task : {route_id}|{text_hash}|{ssml_text[:20]}"
        file_name = self.__construct_file_name(route_id, text_hash)
        out_file_path = self.speech_kit.create_speech_file(ssml_text, file_name)
        if not out_file_path:
            raise RuntimeError(f"Sth went wrong {route_id}{file_name}")
        main_logger.log(f"Result: {out_file_path} {task_info} done (file: {file_name})")
        return file_name

    def __construct_file_name(self, route_id: str, text_hash: str) -> str:
        """
        Constructs file name by route_id and text_hash
        :param text_hash: hash chosen to represent content of file
        :return: name of file constructed from route_id and text_hash
        """
        now = time.time()
        sep = self.settings.FILE_PARTS_SEPARATOR
        return f"{route_id}{sep}{text_hash}{sep}{now}.mp3"


app_main_methods = AppMethods(speech_kit_processor, app_settings)
