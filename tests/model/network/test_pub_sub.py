from pynet.model.network.channels.publishers import Publishers
from pynet.model.network.channels.subscribers import Subscribers
from pynet.model.network.url import Url, BaseUrl
from dataclassy import dataclass
import concurrent.futures
import pytest
import time

DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def usleep(microsecond):
    time.sleep(microsecond / 1000000.0)


@dataclass(unsafe_hash=True, slots=True)
class PubSubTestCase:
    url: BaseUrl
    compression: bool
    data: object


# Actions for connection bind
# publisher, pusher
def thread_publisher(test_case: PubSubTestCase):
    p = Publishers('Test')
    p.add(f'Test-{type(test_case.url).__name__}', test_case.url)
    usleep(8000)
    res = p.publish(test_case.data, compression=test_case.compression)
    usleep(8000)
    p.close()
    return res[0]


# # Actions for connection connect
# # subscriber, puller
def thread_subscriber(test_case: PubSubTestCase):
    s = Subscribers('Test')
    s.add(f'Test-{type(test_case.url).__name__}', test_case.url)
    data = s.receive()
    s.close()
    return data[0]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [  # Without Compression
                             (PubSubTestCase(url=Url.Remote(), compression=False, data=DATA)),
                             (PubSubTestCase(url=Url.Local(), compression=False, data=DATA)),
                             (PubSubTestCase(url=Url.Local(local_type=Url.LocalType().ipc), compression=False,
                                             data=DATA)),
                             # With Compression
                             (PubSubTestCase(url=Url.Remote(), compression=True, data=DATA)),
                             (PubSubTestCase(url=Url.Local(), compression=True, data=DATA)),
                             (PubSubTestCase(url=Url.Local(local_type=Url.LocalType().ipc), compression=True,
                                             data=DATA)),
                         ])
def test_channel_pub_sub(test_case):
    # Parallel Task
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_pub = executor.submit(thread_publisher, test_case)
        future_sub = executor.submit(thread_subscriber, test_case)
        res_pub = future_pub.result()
        res_sub = future_sub.result()

        assert res_pub
        assert res_sub == test_case.data
