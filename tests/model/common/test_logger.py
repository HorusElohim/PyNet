from pynet.model.common import Logger

TEST_LOGGER = Logger('Test-Logger')


def test_logger():
    TEST_LOGGER.log.debug('[1]')


def test_logger_from_other():
    logger = Logger(logger_other=TEST_LOGGER)
    assert logger is not None
    logger.log.debug('[2]')


def test_logger_file():
    assert TEST_LOGGER.logger_file_path.exists()


def test_logger_change_name():
    logger = Logger(logger_other=TEST_LOGGER)
    new_name = 'Test-Logger-NameChanged'
    assert logger is not None
    logger.log.debug('[3]')
    assert logger.logger_file_path.exists()
    logger.logger_name = new_name
    logger.log.debug('[4] debug logger has change name')
    with open(logger.logger_file_path, 'r') as fd:
        res = fd.read()
    assert new_name in res


def test_logger_change_file_name():
    logger = Logger(logger_other=TEST_LOGGER)
    new_name = 'Test-Logger-FileChanged'
    logger.log.debug('[5]')
    logger.logger_file_name = new_name
    logger.log.debug('[6] debug logger has change file')
    assert logger.logger_file_path.exists()
