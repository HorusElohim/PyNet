from pynet.model.network.channels.publishers import Publishers
from pynet.model.network.channels.subscribers import Subscribers
from pynet.model.network.url import Url, BaseUrl, RemoteUrl
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
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


# WORKER
class PubSubWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PubSubTestCase = test_case
        self.result = None


# Actions for connection bind
# publisher
class PublisherWorker(PubSubWorker):
    def run(self) -> None:
        if isinstance(self.test_case.url, RemoteUrl):
            self.test_case.url.ip = '*'
        p = Publishers('Test')
        p.add(f'Test-{type(self.test_case.url).__name__}', self.test_case.url)
        usleep(12500)
        res = p.publish(self.test_case.data, compression=self.test_case.compression)
        res = p.publish(self.test_case.data, compression=self.test_case.compression)
        res = p.publish(self.test_case.data, compression=self.test_case.compression)
        usleep(8000)
        p.close()
        self.result = res[0]


# # Actions for connection connect
# # subscriber
class SubscriberWorker(PubSubWorker):
    def run(self) -> None:
        s = Subscribers('Test')
        s.add(f'Test-{type(self.test_case.url).__name__}', self.test_case.url)
        data = s.receive()
        s.close()
        self.result = data[0]


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
    workers = [PublisherWorker(test_case), SubscriberWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result == test_case.data
