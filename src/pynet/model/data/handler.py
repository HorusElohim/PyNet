from pathlib import Path
from typing import Union, BinaryIO, Generator
from os import mkdir

from . import Bucket, MapBuckets
from ..common import Size

DEFAULT_BUCKET_SIZE = 2 ** 8


class FileDoNotExistException(Exception):
    pass


class FileHandler:
    __slots__ = 'target', 'bucket_map', 'bucket_size'

    def __init__(self, target: Union[Path, str], bucket_size: int = DEFAULT_BUCKET_SIZE, build: bool = False) -> None:
        target = FileHandler.get_path(target)

        self.target = target
        self.bucket_map = MapBuckets(target.name)
        self.bucket_size = bucket_size

        if build:
            self.build_map()

    def __bool__(self) -> bool:
        return self.check_integrity_with_file(self.target)

    @staticmethod
    def read_by_chuck(file_descriptor: BinaryIO, bucket_size: int = DEFAULT_BUCKET_SIZE) -> Generator[bytes, None, None]:
        while True:
            data = file_descriptor.read(bucket_size)
            if not data:
                break
            yield data

    @staticmethod
    def create_bucket(data: bytes) -> Bucket:
        return Bucket(data)

    @staticmethod
    def build_bucket_map(path: Union[str, Path], bucket_size: int = DEFAULT_BUCKET_SIZE) -> MapBuckets:
        path = FileHandler.get_path(path)
        bucket_map = MapBuckets(path.name)
        with open(path, 'rb') as fd:
            for chunk in FileHandler.read_by_chuck(fd, bucket_size):
                bucket_map.add(FileHandler.create_bucket(chunk))
        return bucket_map

    def build_map(self) -> None:
        self._safe_valid_guard()
        self.bucket_map = FileHandler.build_bucket_map(self.target, self.bucket_size)

    def get_diff_map_bucket_with_file(self, path: Union[str, Path]) -> MapBuckets:
        path = FileHandler.get_path(path)
        if not path.exists():
            raise FileDoNotExistException()
        return self.bucket_map - FileHandler.build_bucket_map(path, self.bucket_size)

    def check_integrity_with_file(self, path: Union[str, Path]) -> bool:
        path = FileHandler.get_path(path)
        if not path.exists():
            raise FileDoNotExistException()
        return len(self.get_diff_map_bucket_with_file(path)) == 0

    @property
    def is_valid(self) -> bool:
        return self.target.exists()

    @property
    def file_size(self) -> int:
        return Size.file_size(str(self.target.absolute()))

    def _safe_valid_guard(self) -> None:
        if not self.is_valid:
            raise FileDoNotExistException()

    @staticmethod
    def get_path(path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            return Path(path)
        elif isinstance(path, Path):
            return path

    @staticmethod
    def ensure_path(path: Path) -> None:
        if not path.parent.exists():
            mkdir(path.parent)


class FolderHandler:
    pass
