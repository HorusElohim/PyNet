from pynet.model import Bucket, MapBuckets


def test_bucket():
    test_data1 = bytes('test-binaries-data-1', 'utf8')
    test_data2 = bytes('test-binaries-data-2', 'utf8')
    b1 = Bucket(test_data1)
    b2 = Bucket(test_data1)
    b3 = Bucket(test_data2)
    assert len(b1) == len(test_data1)
    assert hash(b1) == hash(test_data1)
    assert b1 == b2
    assert not b1 == b3


def test_hashmap_from_bytes():
    test_data1 = bytes('test-binaries-data-1', 'utf8')
    test_data2 = bytes('test-binaries-data-2', 'utf8')
    b1 = Bucket(test_data1)
    b2 = Bucket(test_data2)
    bucket_map = MapBuckets('test-binaries-data-1')
    bucket_map.add(test_data1)
    bucket_map.add(test_data2)
    assert not b1
    assert not b2
    assert bucket_map.size == len(b1) + len(b2)
    assert len(bucket_map) == 2
    indexes = list(bucket_map('index'))
    assert bucket_map.buckets[indexes[0]] == b1
    assert bucket_map.buckets[indexes[1]] == b2
    assert not bucket_map


def test_hashmap_from_bucket():
    test_data1 = bytes('test-binaries-data-1', 'utf8')
    test_data2 = bytes('test-binaries-data-2', 'utf8')
    b1 = Bucket(test_data1)
    b1.set_done()
    b2 = Bucket(test_data2)
    b2.set_done()
    bucket_map = MapBuckets('test-binaries-data-1')
    bucket_map.add(b1)
    bucket_map.add(b2)
    assert b1
    assert b2
    assert bucket_map.size == len(b1) + len(b2)
    assert len(bucket_map) == 2
    buckets = list(bucket_map('bucket'))
    assert buckets[0] == b1
    assert buckets[1] == b2
    assert bucket_map


def test_hashmap_override_subtraction_operator():
    test_data1 = bytes('test-binaries-data-1', 'utf8')
    test_data2 = bytes('test-binaries-data-2', 'utf8')
    b1 = Bucket(test_data1)
    b2 = Bucket(test_data2)
    bucket_map1 = MapBuckets('test-binaries-data-1')
    bucket_map2 = MapBuckets('test-binaries-data-1')
    bucket_map1.add(b1)
    bucket_map2.add(b2)
    bucket_map3 = bucket_map1 - bucket_map2
    assert len(bucket_map3) == 1
    assert bucket_map3.buckets.pop(1) == b1
