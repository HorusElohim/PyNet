from __future__ import annotations
from . import Singleton
import logging
from typing import Union
from enum import IntEnum

# Reduce Logger Messages
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Formatter
CONSOLE_FORMATTER = logging.Formatter(fmt="%(levelname)-8s %(asctime)s %(name)s::%(funcName)s %(message)s")
FILE_FORMATTER = logging.Formatter(
    fmt="%(levelname)-8s\t%(asctime)s.%(msecs)03d\t"
        "%(process)d|%(thread)d:%(threadName)s\t"
        "%(filename)s:%(lineno)d %(name)s::%(funcName)s\t"
        "%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")


class LoggerCannotWorkIfBothConsoleAndFileAreDisabled(Exception):
    """
        Logger Not Initialized Exception
    """

    def __init__(self) -> None:
        print("[ERROR] Call on Logger not Initialized")


class LoggerLevel(IntEnum):
    """
        Logger Level Enum
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


class Logger:
    """
    Logger Base Class

    Examples:
        >>> logger = Logger()
        >>> logger.log.debug('message')
        >>> class Test(Logger):
        >>>     pass
        >>> t = Test()
        >>> t.log.debug('message')
    """

    __logger: Union[logging.Logger, None] = None
    __logger_console_active: bool = True
    __logger_console_level: LoggerLevel = DEFAULT_CONSOLE_LEVEL
    __logger_file_active: bool = True
    __logger_file_level: LoggerLevel = DEFAULT_FILE_LEVEL
    __logger_file_name: str = DEFAULT_FILE_NAME

    def __clean_logger(self) -> None:
        """
        Clean Logger Handlers
        """
        list(map(self.__logger.removeHandler, self.__logger.handlers))
        list(map(self.__logger.removeFilter, self.__logger.filters))
        self.__logger.setLevel(logging.DEBUG)

    def __construct_logger(self) -> None:
        """
        Construct dedicated logger
        """
        if self.__logger_console_active or self.__logger_file_active:
            # Get dedicated Class logger
            self.__logger = logging.getLogger(self.__class__.__name__)
            # Clean all the hereditary logger
            self.__clean_logger()
            # Activate console logger handler
            if self.__logger_console_active:
                self.__construct_console_logger()
            if self.__logger_file_active:
                self.__construct_file_logger()

    def __construct_console_logger(self):
        # define a Handler which writes sys.stdout
        console_handler = logging.StreamHandler()
        # Set log level
        console_handler.setLevel(self.__logger_console_level)
        # tell the handler to use this format
        console_handler.setFormatter(CONSOLE_FORMATTER)
        # add the handler to the root logger
        self.__logger.addHandler(console_handler)

    def __construct_file_logger(self):
        file_handler = logging.FileHandler(self.__logger_file_name)
        file_handler.setLevel(self.__logger_file_level)
        file_handler.setFormatter(FILE_FORMATTER)
        self.__logger.addHandler(file_handler)

    @property
    def log(self) -> Union[logging.Logger, None]:
        if self.__logger is None:
            self.__construct_logger()
        if self.__logger is None:
            raise LoggerCannotWorkIfBothConsoleAndFileAreDisabled()
        return self.__logger
