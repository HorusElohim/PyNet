from pynet.model import FileHandler, FolderHandler, Bucket, MapBuckets
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
    assert fh.check_integrity_file(TEST_FILE_PATH.absolute())


def test_file_handler_save():
    fh = FileHandler(TEST_FILE_PATH.absolute(), build=True)
    fh.save_bucket_map()
    assert (fh.target.parent / (fh.bucket_map.filename + '.buckets')).exists()


def test_file_handler_load():
    fh = FileHandler(TEST_FILE_PATH.absolute())
    fh.load_map()
    assert fh.is_valid
    assert fh.file_size == 31661
    assert len(fh.bucket_map) == 124
    assert fh.bucket_map.size == 31661
    assert fh
    assert fh.check_integrity_file(TEST_FILE_PATH.absolute())
