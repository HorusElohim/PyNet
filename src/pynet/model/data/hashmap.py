from typing import Dict, Union
from collections import OrderedDict


class Bucket:
    __slots__ = 'hash', 'size', 'done'

    def __init__(self, byte: bytes):
        self.hash = hash(byte)
        self.size = len(byte)
        self.done: bool = False

    def __hash__(self):
        return self.hash

    def __bool__(self):
        return self.done

    def __len__(self):
        return self.size

    def __eq__(self, other):
        if not isinstance(other, Bucket):
            return False
        return hash(other) == hash(self)

    def __str__(self):
        return f'<Bucket:{hash(self)}/{len(self)}>'

    def set_done(self):
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

    def __init__(self, filename: str):
        self.buckets: OrderedDict[int, Bucket] = OrderedDict()
        self.filename: str = filename

    def __eq__(self, other):
        return hash(other) == hash(self)

    def __hash__(self):
        return hash(self.buckets) + hash(self.filename)

    def __bool__(self):
        return all(map(bool, list(self.__call__('bucket'))))

    def __add__(self, other: 'MapBuckets'):
        if not isinstance(other, MapBuckets):
            raise MapBucketInvalidOperationWithOtherTypeDifferentThenMapBucketException
        if other.filename != self.filename:
            raise MapBucketInvalidOperationWithDifferentMapBucketTargetFile()

        new_map_bucket = MapBuckets(self.filename)
        new_map_bucket.buckets = self.buckets.copy()
        new_map_bucket.buckets.update(other.buckets)
        return new_map_bucket

    def __sub__(self, other: 'MapBuckets'):
        if not isinstance(other, MapBuckets):
            raise MapBucketInvalidOperationWithOtherTypeDifferentThenMapBucketException
        if other.filename != self.filename:
            raise MapBucketInvalidOperationWithDifferentMapBucketTargetFile()

        new_map_bucket = MapBuckets(self.filename)
        new_map_bucket.buckets = dict(self.buckets.items() - other.buckets.items())
        return new_map_bucket

    @property
    def size(self):
        return sum(len(v) for _, v in self.buckets.items())

    def __len__(self):
        return len(self.buckets)

    def add(self, item: Union[bytes, Bucket]):
        if isinstance(item, Bucket):
            self._add_from_bucket(item)
        elif isinstance(item, bytes):
            self._add_from_bytes(item)

    def _add_from_bucket(self, bucket: Bucket):
        if not isinstance(bucket, Bucket):
            raise MapBucketInvalidInputFromBucketException()

        current_index = max(self.buckets.keys()) if len(self.buckets) > 0 else 0

        self.buckets[current_index + 1] = bucket

    def _add_from_bytes(self, byte: bytes):
        if not isinstance(byte, bytes):
            raise MapBucketInvalidInputFromByteException()
        self._add_from_bucket(Bucket(byte))

    def __call__(self, iter_on='all'):
        for i, bucket in self.buckets.items():
            if 'index' == iter_on:
                yield i
            elif 'bucket' == iter_on:
                yield bucket
            elif 'all' == iter_on:
                yield i, bucket

    def __str__(self):
        return f'<MapBuckets:[{self.filename}/{[str(b) for b in self.__call__()]}]>'
