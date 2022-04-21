from __future__ import annotations
from . import Singleton
import logging
from typing import Union
from enum import IntEnum


class LoggerNotInitialized(Exception):
    """
        Logger Not Initialized Exception
    """

    def __init__(self) -> None:
        print("[ERROR] Call on Logger not Initialized")


class LoggerLevel(IntEnum):
    """
        Logger Level Enum
        * CRITICAL
        * FATAL
        * ERROR
        * WARNING
        * WARN
        * INFO
        * DEBUG
        * NOTSET
    """
    CRITICAL = 50
    FATAL = 50
    ERROR = 40
    WARNING = 30
    WARN = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


DEFAULT_LOGGER_NAME = "PyNet"
DEFAULT_FILE_NAME = f"{DEFAULT_LOGGER_NAME}.log"
DEFAULT_FILE_LEVEL = LoggerLevel.DEBUG
DEFAULT_CONSOLE_LEVEL = LoggerLevel.DEBUG


class Logger(metaclass=Singleton):
    """
    Logger Singleton Class

    Args:
            filelog: Flag activate file logging.
            logfile: Filename to store the log.
            file_log_level: File log level.
            consolelog: Flag activate console log.
            console_log_level: Console log level.
    """
    __logger: Union[logging.Logger, None] = None

    def __init__(self, filelog: bool = True,
                 logfile: str = DEFAULT_FILE_NAME,
                 file_log_level: LoggerLevel = DEFAULT_FILE_LEVEL,
                 consolelog: bool = True,
                 console_log_level: LoggerLevel = DEFAULT_CONSOLE_LEVEL) -> None:

        # reduce informational logging
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        # initialize class logger
        self.__logger = logging.getLogger(DEFAULT_LOGGER_NAME)
        list(map(self.__logger.removeHandler, self.__logger.handlers))
        list(map(self.__logger.removeFilter, self.__logger.filters))
        self.__logger.setLevel(logging.DEBUG)

        if not consolelog and not filelog:
            self.__logger.disabled = True

        if consolelog:
            # set a format which is simpler for console use
            console_formatter = logging.Formatter("%(asctime)s %(message)s")
            # define a Handler which writes sys.stdout
            console_handler = logging.StreamHandler()
            # Set log level
            console_handler.setLevel(console_log_level)

            # tell the handler to use this format
            console_handler.setFormatter(console_formatter)
            # add the handler to the root logger
            self.__logger.addHandler(console_handler)

        if filelog:
            # set up logging to file
            file_formatter = logging.Formatter(
                fmt="%(asctime)s.%(msecs)03d\t"
                    "%(process)d|%(thread)d:%(threadName)s\t"
                    "%(filename)s:%(lineno)d in %(funcName)s\t"
                    "%(levelname)-8s\t%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel(file_log_level)
            file_handler.setFormatter(file_formatter)
            self.__logger.addHandler(file_handler)

    def __call__(self) -> logging.Logger:
        if self.__logger is None:
            raise LoggerNotInitialized()
        return self.__logger
