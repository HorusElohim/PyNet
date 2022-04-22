from pynet.model.common import Logger
from pynet.model.common.logger import DEFAULT_FILE_NAME
from pathlib import Path


def test_logger_creation():
    logger = Logger()
    assert logger is not None
    logger().debug('debug')


def test_logger_file():
    logger = Logger()
    assert logger is not None
    logger().debug('debug')
    assert Path(Path().cwd() / DEFAULT_FILE_NAME).exists()
