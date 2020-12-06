import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future

from configs.app_config import CONFIG
from server.utils.logger import log, log_exception, log_error
from server.utils.mp3_storage import StorageValue
from server.utils.speech_processor import CURRENT_PROCESSOR
from server.utils.yandex_speech.yandex_speech_processor import YandexApiException

EXECUTOR = ThreadPoolExecutor(CONFIG.concurrency_lvl)
log(f"Created executor concurrency_lvl : {CONFIG.concurrency_lvl}\n")


def submit(task, callback, *args, **kwargs) -> Future:
    future = EXECUTOR.submit(task, *args, **kwargs)
    future.add_done_callback(callback)
    return future


def shutdown():
    EXECUTOR.shutdown()


def get_file_name(route_id: str, text_hash: str) -> str:
    now = time.time()
    sep = CONFIG.file_parts_separator
    return f"{route_id}{sep}{text_hash}{sep}{now}.mp3"


@log_exception
def route_to_audio_task(value: StorageValue, route_id: str, text: str, text_hash: str):
    task_info = f"route_to_audio_task : {route_id}|{text_hash}|{text[:20]}"
    try:
        file_name = get_file_name(route_id, text_hash)
        res, out_file_path = CURRENT_PROCESSOR.create_speech_file(text, file_name)
        if not res:
            raise RuntimeError(f"Sth went wrong {route_id}{file_name}")
        value.file_name = file_name
        value.state = StorageValue.STATE_DONE
        log(f"Result: {res} {task_info} done (file: {file_name})")
    except YandexApiException as exp:
        log_error(f"{task_info} broken on Yandex API, exception {exp}")
        value.state = StorageValue.STATE_BROKEN
    except Exception as exp:
        log_error(f"{task_info} broken, exception {exp}")
        value.state = StorageValue.STATE_BROKEN


@log_exception
def route_to_audio_callback(future):
    pass


if __name__ == '__main__':
    @log_exception
    def task(a, b, d):
        log(f"{a} {b} {d}")
        time.sleep(2)
        raise RuntimeError("Bad thing happened")


    for i in range(100):
        def callback(future, i=i):
            log(future.result())
            log("got callback " + str(i))


        future = submit(task, callback, i, 2, d=3)
