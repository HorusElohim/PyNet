from pynet.model import Logger


def test_logger_creation():
    logger = Logger()
    assert logger is not None
    logger().debug('debug')
