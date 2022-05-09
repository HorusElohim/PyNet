# Copyright (C) 2022 HorusElohim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from __future__ import annotations
import logging
from typing import Union
from enum import IntEnum
from threading import Lock
from . import today
from ... import LOG_PATH

SAFE_LOGGER_LOCK = Lock()

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
DEFAULT_CONSOLE_ACTIVE = False
DEFAULT_FILE_ACTIVE = True
DEFAULT_FILE_NAME = f"{DEFAULT_LOGGER_NAME}.{today()}.log"
DEFAULT_FILE_PATH = LOG_PATH / DEFAULT_FILE_NAME
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

    def __init__(self, name: str = '') -> None:
        self.__logger_name = name
        self.__logger_console_active: bool = DEFAULT_CONSOLE_ACTIVE
        self.__logger_console_level: LoggerLevel = DEFAULT_CONSOLE_LEVEL
        self.__logger_file_active: bool = DEFAULT_FILE_ACTIVE
        self.__logger_file_level: LoggerLevel = DEFAULT_FILE_LEVEL
        self.__logger_file_name: str = DEFAULT_FILE_PATH
        self.__logger: Union[logging.Logger, None] = None

    def __clean_logger(self) -> None:
        """
        Clean Logger Handlers
        """
        assert isinstance(self.__logger, logging.Logger)
        list(map(self.__logger.removeHandler, self.__logger.handlers))
        list(map(self.__logger.removeFilter, self.__logger.filters))
        self.__logger.setLevel(logging.DEBUG)

    def __construct_logger(self) -> None:
        """
        Construct dedicated logger
        """
        if self.__logger_console_active or self.__logger_file_active:
            # Get dedicated Class logger
            if not self.__logger_name:
                self.__logger_name = self.__class__.__name__
            self.__logger: logging.Logger = logging.getLogger(self.__logger_name)  # type: ignore[no-redef]
            self.__logger.propagate = False
            # Check already created
            if self.__logger.hasHandlers():
                return None
            # Clean all the hereditary logger
            self.__clean_logger()
            # Activate console logger handler
            if self.__logger_console_active:
                self.__construct_console_logger()
            if self.__logger_file_active:
                self.__construct_file_logger()

    def __construct_console_logger(self) -> None:
        assert isinstance(self.__logger, logging.Logger)
        # define a Handler which writes sys.stdout
        console_handler = logging.StreamHandler()
        # Set log level
        console_handler.setLevel(self.__logger_console_level)
        # tell the handler to use this format
        console_handler.setFormatter(CONSOLE_FORMATTER)
        # add the handler to the root logger
        self.__logger.addHandler(console_handler)

    def __construct_file_logger(self) -> None:
        assert isinstance(self.__logger, logging.Logger)
        file_handler = logging.FileHandler(self.__logger_file_name)
        file_handler.setLevel(self.__logger_file_level)
        file_handler.setFormatter(FILE_FORMATTER)
        self.__logger.addHandler(file_handler)

    @property
    def log(self) -> logging.Logger:
        if self.__logger is None:
            SAFE_LOGGER_LOCK.acquire()
            self.__construct_logger()
            SAFE_LOGGER_LOCK.release()
        if self.__logger is None:
            raise LoggerCannotWorkIfBothConsoleAndFileAreDisabled()
        assert isinstance(self.__logger, logging.Logger)
        return self.__logger
