from pynet.model.common import Logger
from pynet.model.common.logger import DEFAULT_FILE_PATH


def test_logger_creation():
    logger = Logger()
    assert logger is not None
    logger.log.debug('debug')


def test_logger_file():
    logger = Logger()
    assert logger is not None
    logger.log.debug('debug')
    assert DEFAULT_FILE_PATH.exists()
