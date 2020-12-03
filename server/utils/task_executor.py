import time
from concurrent.futures import ThreadPoolExecutor

from server.app_config import CONFIG
from server.utils.logger import log

EXECUTOR = ThreadPoolExecutor(CONFIG.concurrency_lvl)
log(f"Created executor concurrency_lvl : {CONFIG.concurrency_lvl}")


def submit(task, callback, *args, **kwargs):
    future = EXECUTOR.submit(task, *args, **kwargs)
    future.add_done_callback(callback)
    return future


def shutdown():
    EXECUTOR.shutdown()


if __name__ == '__main__':
    def task(a, b, d):
        log(f"{a} {b} {d}")
        time.sleep(100)


    for i in range(100):
        def callback(future, i=i):
            log("got callback " + str(i))


        future = submit(task, callback, i, 2, d=3)
