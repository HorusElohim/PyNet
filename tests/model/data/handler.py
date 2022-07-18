from pynet.model import FileHandler, FolderHandler
from pathlib import Path

TEST_FILE_PATH = Path(__file__).parent / 'test_data.txt'


def test_file_handler():
    fh = FileHandler(TEST_FILE_PATH.absolute())
    fh.build_map()
    assert fh.is_valid
    assert fh.file_size == 31661
    assert len(fh.bucket_map) == 124
    assert fh.bucket_map.size == 31661
    assert fh
    assert fh.check_integrity_with_file(TEST_FILE_PATH.absolute())
