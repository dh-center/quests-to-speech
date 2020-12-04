import logging
import sys
import time
from functools import wraps
from logging.handlers import RotatingFileHandler

BYTES_IN_MEGABYTE = (2 ** 20)

logging.basicConfig(filename='log.log', level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

formatter = logging.Formatter('%(asctime)s : %(message)s', '%b %d %H:%M:%S')
formatter.converter = time.gmtime

__LOGGER = logging.getLogger("Rotating Log")

file_handler = RotatingFileHandler('log.log', maxBytes=20 * BYTES_IN_MEGABYTE, backupCount=2)
file_handler.setFormatter(formatter)
__LOGGER.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
# do not forget to spool both stdout and stderr > /dev/null 2>&1
__LOGGER.addHandler(console_handler)


def log_error(message):
    __LOGGER.exception(f"Error happened {message}")


def log(messages):
    __LOGGER.info(messages)


# # print log
# LOG_LOCK = threading.RLock()
#
# def log(*msg):
#     with LOG_LOCK:
#         print(*msg, sep=" : ")

# exceptions handle decorator
def log_exception(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as exp:
            log(f"Exception happened : {exp}")

    return wrapper
