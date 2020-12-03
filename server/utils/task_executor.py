import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future

from server.app_config import CONFIG
from server.utils.logger import log, log_exception
from server.utils.mp3_storage import StorageValue
from server.utils.speech_processor import CURRENT_PROCESSOR

EXECUTOR = ThreadPoolExecutor(CONFIG.concurrency_lvl)
log(f"Created executor concurrency_lvl : {CONFIG.concurrency_lvl}\n")


def submit(task, callback, *args, **kwargs) -> Future:
    future = EXECUTOR.submit(task, *args, **kwargs)
    future.add_done_callback(callback)
    return future


def shutdown():
    EXECUTOR.shutdown()


@log_exception
def route_to_audio_task(value: StorageValue, route_id: str, text: str, text_hash: str):
    task_info = f"route_to_audio_task : {route_id}|{text_hash}|{text[:20]}"
    try:
        value.state = StorageValue.STATE_DONE
        CURRENT_PROCESSOR.create_speech_file()
        # TODO get audio, create file
        log(f"{task_info} done")
    except Exception as exp:
        log(f"{task_info} broken, exception {exp}")


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
