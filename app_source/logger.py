import logging
import os
import sys
import time
from functools import wraps
from logging import Logger
from logging.handlers import RotatingFileHandler

from app_source.app_settings import APP_SETTINGS

BYTES_IN_MEGABYTE = (2 ** 20)


class AppLogger:
    """
    Class to configure logging of application
    """
    main_logger: Logger

    def __init__(self):
        # initialise logger folder if it is needed
        if not os.path.isdir(APP_SETTINGS.DATA_FOLDER):
            os.makedirs(APP_SETTINGS.DATA_FOLDER)

        # for the root logger (to separate server messages)
        logging.basicConfig(filename=os.path.join(APP_SETTINGS.DATA_FOLDER, 'server.log'), level=logging.INFO,
                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        # configure formatter
        formatter = logging.Formatter('%(asctime)s : %(message)s', '%b %d %H:%M:%S')
        formatter.converter = time.gmtime

        # specify logger
        self.main_logger = logging.getLogger("Main logger")

        # collect handlers
        self.handlers = []
        file_handler = RotatingFileHandler(
            os.path.join(APP_SETTINGS.DATA_FOLDER, 'app.log'), maxBytes=20 * BYTES_IN_MEGABYTE, backupCount=2
        )
        console_handler = logging.StreamHandler(sys.stdout)

        self.handlers.append(file_handler)
        self.handlers.append(console_handler)

        # configure handlers
        for handler in self.handlers:
            handler.setFormatter(formatter)
            self.main_logger.addHandler(handler)

        self.main_logger.setLevel(logging.INFO)

    def add_additional_loggers(self, logger: Logger):
        """
        Add logger current available handlers
        :param logger: to add handlers to
        """
        for handler in self.handlers:
            logger.addHandler(handler)

    def log_error(self, message: str):
        """
        log method for exceptions
        :param message: log message
        """
        self.main_logger.exception(message)

    def log(self, message: str):
        """
        :param message: log message
        """
        self.main_logger.info(message)

    def log_exception_decorator(self, fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except Exception as exp:
                self.log(f"Exception happened : {exp}")

        return wrapper


LOGGER = AppLogger()
