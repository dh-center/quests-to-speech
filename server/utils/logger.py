import threading

LOG_LOCK = threading.RLock()


def log(*msg):
    with LOG_LOCK:
        print(*msg, sep=" : ")
