import hashlib
import time

from app_source.app_settings import settings
from app_source.logger import log
from yandex_speech_kit.speech_kit import create_speech_file


def hash_text(text: str) -> str:
    sha = hashlib.sha256()
    sha.update(str.encode(text))
    return f"{sha.hexdigest()}-{len(text)}"


def get_file_name(route_id: str, text_hash: str) -> str:
    now = time.time()
    sep = settings.file_parts_separator
    return f"{route_id}{sep}{text_hash}{sep}{now}.mp3"


def route_to_audio(route_id: str, text: str, text_hash: str) -> str:
    task_info = f"route_to_audio_task : {route_id}|{text_hash}|{text[:20]}"
    file_name = get_file_name(route_id, text_hash)
    out_file_path = create_speech_file(text, file_name)
    if not out_file_path:
        raise RuntimeError(f"Sth went wrong {route_id}{file_name}")
    log(f"Result: {out_file_path} {task_info} done (file: {file_name})")
    return file_name

