from typing import Union, Tuple, Generator
from collections import OrderedDict


class Bucket:
    __slots__ = 'hash', 'size', 'done'

    def __init__(self, byte: bytes):
        self.hash = hash(byte)
        self.size = len(byte)
        self.done: bool = False

    def __hash__(self) -> int:
        return self.hash

    def __bool__(self) -> bool:
        return self.done

    def __len__(self) -> int:
        return self.size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bucket):
            return False
        return hash(other) == hash(self)

    def __str__(self) -> str:
        return f'<Bucket:{hash(self)}/{len(self)}>'

    def set_done(self) -> None:
        self.done = True


class MapBucketInvalidInputFromBucketException(Exception):
    pass


class MapBucketInvalidInputFromByteException(Exception):
    pass


class MapBucketInvalidOperationWithOtherTypeDifferentThenMapBucketException(Exception):
    pass


class MapBucketInvalidOperationWithDifferentMapBucketTargetFile(Exception):
    pass


class MapBuckets:
    __slots__ = 'buckets', 'filename'

    def __init__(self, filename: str) -> None:
        self.buckets: OrderedDict[int, Bucket] = OrderedDict()
        self.filename: str = filename

    def __eq__(self, other: object) -> bool:
        return hash(other) == hash(self)

    def __hash__(self) -> int:
        return hash(self.buckets) + hash(self.filename)

    def __bool__(self) -> bool:
        return all(map(bool, list(self.__call__('bucket'))))

    def __add__(self, other: 'MapBuckets') -> 'MapBuckets':
        if not isinstance(other, MapBuckets):
            raise MapBucketInvalidOperationWithOtherTypeDifferentThenMapBucketException
        if other.filename != self.filename:
            raise MapBucketInvalidOperationWithDifferentMapBucketTargetFile()

        new_map_bucket = MapBuckets(self.filename)
        new_map_bucket.buckets = self.buckets.copy()
        new_map_bucket.buckets.update(other.buckets)
        return new_map_bucket

    def __sub__(self, other: 'MapBuckets') -> 'MapBuckets':
        if not isinstance(other, MapBuckets):
            raise MapBucketInvalidOperationWithOtherTypeDifferentThenMapBucketException
        if other.filename != self.filename:
            raise MapBucketInvalidOperationWithDifferentMapBucketTargetFile()

        new_map_bucket = MapBuckets(self.filename)
        new_map_bucket.buckets = OrderedDict(self.buckets.items() - other.buckets.items())
        return new_map_bucket

    @property
    def size(self) -> int:
        return sum(len(v) for _, v in self.buckets.items())

    def __len__(self) -> int:
        return len(self.buckets)

    def add(self, item: Union[bytes, Bucket]) -> None:
        if isinstance(item, Bucket):
            self._add_from_bucket(item)
        elif isinstance(item, bytes):
            self._add_from_bytes(item)

    def _add_from_bucket(self, bucket: Bucket) -> None:
        if not isinstance(bucket, Bucket):
            raise MapBucketInvalidInputFromBucketException()

        current_index = max(self.buckets.keys()) if len(self.buckets) > 0 else 0

        self.buckets[current_index + 1] = bucket

    def _add_from_bytes(self, byte: bytes) -> None:
        if not isinstance(byte, bytes):
            raise MapBucketInvalidInputFromByteException()
        self._add_from_bucket(Bucket(byte))

    def __call__(self, iter_on: str = 'all') -> Generator[Union[int, Bucket, Tuple[int, Bucket]], None, None]:
        for i, bucket in self.buckets.items():
            if 'index' == iter_on:
                yield i
            elif 'bucket' == iter_on:
                yield bucket
            elif 'all' == iter_on:
                yield i, bucket

    def __str__(self) -> str:
        return f'<MapBuckets:[{self.filename}/{[str(b) for b in self.__call__()]}]>'
