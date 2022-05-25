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
from typing import Union, Tuple
from enum import IntEnum
from threading import Lock
from pathlib import Path
from . import today
from ... import LOG_PATH, mkdir
import wandb

SAFE_LOGGER_LOCK = Lock()

# Reduce Logger Messages
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Formatter
CONSOLE_FORMATTER = logging.Formatter(fmt="%(levelname)-8s %(asctime)s (%(name)s) %(message)s")
FILE_FORMATTER = logging.Formatter(
    fmt="%(levelname)-8s\t%(asctime)s.%(msecs)03d\t"
        "%(process)d|%(thread)d:%(threadName)s\t"
        "%(filename)s:%(lineno)d:%(funcName)s (%(name)s)\t"
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

    def __init__(self, name: str = '',
                 logger_to_console: bool = DEFAULT_CONSOLE_ACTIVE,
                 logger_to_file: bool = DEFAULT_FILE_ACTIVE,
                 logger_root_path: Path = LOG_PATH,
                 logger_folder: Union[str, None] = None,
                 logger_console_level: LoggerLevel = DEFAULT_CONSOLE_LEVEL,
                 logger_file_level: LoggerLevel = DEFAULT_FILE_LEVEL,
                 logger_other: Union[Logger, None] = None,
                 **kwargs) -> None:

        # Attache to same Logger
        if logger_other:
            self._init_logger_from_other(name, logger_other)
        else:
            self._init_new_logger(name, logger_to_console, logger_to_file, logger_root_path, logger_folder, logger_console_level, logger_file_level)

    def _init_new_logger(self, name: str,
                         logger_to_console: bool,
                         logger_to_file: bool,
                         logger_root_path: Path,
                         logger_folder: Union[str, None],
                         logger_console_level: LoggerLevel,
                         logger_file_level: LoggerLevel):
        if logger_folder:
            logger_root_path = logger_root_path / logger_folder

        if not logger_root_path.exists():
            mkdir(logger_root_path)

        self.__logger_name = name if name else self.__class__.__name__
        self.__logger_console_active: bool = logger_to_console
        self.__logger_console_level: LoggerLevel = logger_console_level
        self.__logger_file_active: bool = logger_to_file
        self.__logger_file_level: LoggerLevel = logger_file_level
        self.__logger_root_path: Path = logger_root_path
        self.__logger_file_path: Path = self.__construct_file_path(self.__logger_name)
        self.__logger: Union[logging.Logger, None] = None

    def _init_logger_from_other(self, name: str, logger_other: Logger):
        if name:
            self.__logger_name = name
        else:
            self.__logger_name = logger_other.logger_name
        self.__logger_console_active: bool = logger_other.logger_console_active
        self.__logger_console_level: LoggerLevel = logger_other.logger_console_level
        self.__logger_file_active: bool = logger_other.logger_file_active
        self.__logger_file_level: LoggerLevel = logger_other.logger_file_level
        self.__logger_root_path: Path = logger_other.logger_root_path
        self.__logger_file_path: Path = logger_other.logger_file_path
        self.__logger: Union[logging.Logger, None] = None

    def __reset_logger(self) -> None:
        """
        Reset Logger Handlers
        """
        self.__reset_handlers()
        self.__logger = None

    def __reset_handlers(self) -> None:
        if isinstance(self.__logger, logging.Logger):
            list(map(self.__logger.removeHandler, self.__logger.handlers))
            list(map(self.__logger.removeFilter, self.__logger.filters))
            self.__logger.setLevel(logging.DEBUG)

    def __construct_logger(self) -> None:
        """
        Construct dedicated logger
        """
        if self.__logger_console_active or self.__logger_file_active:
            # SAFE_LOGGER_LOCK.acquire()
            # Get dedicated Class logger
            self.__logger: logging.Logger = logging.getLogger(self.__logger_name)  # type: ignore[no-redef]
            self.__logger.propagate = False
            # Check already created
            if self.__logger.hasHandlers():
                return None
            # Clean all the hereditary logger
            self.__reset_handlers()
            # Activate console logger handler
            if self.__logger_console_active:
                self.__construct_console_logger()
            if self.__logger_file_active:
                self.__construct_file_logger()
            # SAFE_LOGGER_LOCK.release()

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
        file_handler = logging.FileHandler(self.__logger_file_path)
        file_handler.setLevel(self.__logger_file_level)
        file_handler.setFormatter(FILE_FORMATTER)
        self.__logger.addHandler(file_handler)

    def __construct_new_file_name(self, file_name: str) -> str:
        return f'{file_name}.{today()}.log'

    def __construct_file_path(self, file_name: str):
        return self.__logger_root_path / self.__construct_new_file_name(file_name)

    @property
    def log(self) -> logging.Logger:
        if self.__logger is None:
            self.__construct_logger()
        if self.__logger is None:
            raise LoggerCannotWorkIfBothConsoleAndFileAreDisabled()
        assert isinstance(self.__logger, logging.Logger)
        return self.__logger

    def wandb_log(self, *args, **kwargs):
        try:
            wandb.log(*args, **kwargs)
        except wandb.errors.Error as ex:
            self.log.warning('You must call wandb.init() before wandb.log()')

    @property
    def logger_name(self) -> str:
        return self.__logger_name

    @logger_name.setter
    def logger_name(self, name: str):
        self.__reset_logger()
        self.__logger_name = name

    @property
    def logger_console_active(self) -> bool:
        return self.__logger_console_active

    @logger_console_active.setter
    def logger_console_active(self, active: bool):
        self.__reset_logger()
        self.__logger_console_active = active

    @property
    def logger_file_active(self) -> bool:
        return self.__logger_file_active

    @logger_file_active.setter
    def logger_file_active(self, active: bool):
        self.__reset_logger()
        self.__logger_file_active = active

    @property
    def logger_file_level(self) -> LoggerLevel:
        return self.__logger_file_level

    @logger_file_level.setter
    def logger_file_level(self, level: LoggerLevel):
        self.__reset_logger()
        self.__logger_file_level = level

    @property
    def logger_console_level(self) -> LoggerLevel:
        return self.__logger_console_level

    @logger_console_level.setter
    def logger_console_level(self, level: LoggerLevel):
        self.__reset_logger()
        self.__logger_console_level = level

    @property
    def logger_file_path(self) -> Path:
        return self.__logger_file_path

    @property
    def logger_root_path(self) -> Path:
        return self.__logger_root_path

    @logger_root_path.setter
    def logger_root_path(self, root_path: Path):
        self.__reset_logger()
        self.__logger_root_path = root_path
        self.__logger_file_path: Path = self.__construct_file_path(self.__logger_name)

    @property
    def logger_file_name(self) -> str:
        return self.__logger_file_path.name

    @logger_file_name.setter
    def logger_file_name(self, file_name: str):
        self.__reset_logger()
        self.__logger_file_path = self.__construct_file_path(file_name)

    @property
    def share_logger(self) -> Tuple[Path, Path]:
        return self.__logger_file_path, self.__logger_file_path

    def attach_logger(self, other: Logger, name: str = ''):
        if other:
            self.__reset_logger()
            if name:
                self.__logger_name = name
            else:
                self.__logger_name = other.logger_name
            self.__logger_console_active: bool = other.logger_console_active
            self.__logger_console_level: LoggerLevel = other.logger_console_level
            self.__logger_file_active: bool = other.logger_file_active
            self.__logger_file_level: LoggerLevel = other.logger_file_level
            self.__logger_root_path: Path = other.logger_root_path
            self.__logger_file_path: Path = other.logger_file_path
            self.__construct_logger()
