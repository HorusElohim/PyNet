from pynet.model.network.url import Url, BaseUrl
from pynet.model.network.patterns import *
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
from time import sleep
import pytest

DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


@dataclass(unsafe_hash=True, slots=True)
class PatternsTestCase:
    pattern1: Connection
    pattern2: Connection
    wait1: float
    wait2: float
    url1: BaseUrl
    url2: BaseUrl
    data: object
    compression: bool


# Actions for connection bind
# publisher, pusher, pair
class PatternSendWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern1.url = self.test_case.url1
        self.test_case.pattern1.open()
        sleep(self.test_case.wait1)
        self.result = Transmission.send(self.test_case.pattern1, self.test_case.data, compression=self.test_case.compression)
        sleep(self.test_case.wait1)
        self.test_case.pattern1.close()


# # Actions for connection connect
# # subscriber, puller, pair
class PatternReceiveWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern2.url = self.test_case.url2
        self.test_case.pattern2.open()
        sleep(self.test_case.wait2)
        self.result = Transmission.recv(self.test_case.pattern2)
        sleep(self.test_case.wait2)
        self.test_case.pattern2.close()


TestCasesPubSubPushPullServerClient = [
    # Publisher/Subscriber Server/Client
    # No Compression
    PatternsTestCase(pattern1=Publisher('PUB', Connection.SERVER), wait1=0.4, url1=Url.Remote(ip='*'),
                     pattern2=Subscriber('SUB', Connection.CLIENT), wait2=0.4, url2=Url.Remote(),
                     data=DATA, compression=False),
    PatternsTestCase(pattern1=Publisher('PUB', Connection.SERVER), wait1=0.4, url1=Url.Local(),
                     pattern2=Subscriber('SUB', Connection.CLIENT), wait2=0.4, url2=Url.Local(),
                     data=DATA, compression=False),
    PatternsTestCase(pattern1=Publisher('PUB', Connection.SERVER), wait1=0.4, url1=Url.Local(local_type=Url.IPC),
                     pattern2=Subscriber('SUB', Connection.CLIENT), wait2=0.4, url2=Url.Local(local_type=Url.IPC),
                     data=DATA, compression=False),
    # With Compression
    PatternsTestCase(pattern1=Publisher('PUB', Connection.SERVER), wait1=0.4, url1=Url.Remote(ip='*'),
                     pattern2=Subscriber('SUB', Connection.CLIENT), wait2=0.4, url2=Url.Remote(),
                     data=DATA, compression=True),
    PatternsTestCase(pattern1=Publisher('PUB', Connection.SERVER), wait1=0.4, url1=Url.Local(),
                     pattern2=Subscriber('SUB', Connection.CLIENT), wait2=0.4, url2=Url.Local(),
                     data=DATA, compression=True),
    PatternsTestCase(pattern1=Publisher('PUB', Connection.SERVER), wait1=0.4, url1=Url.Local(local_type=Url.IPC),
                     pattern2=Subscriber('SUB', Connection.CLIENT), wait2=0.4, url2=Url.Local(local_type=Url.IPC),
                     data=DATA, compression=True),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesPubSubPushPullServerClient)
def test_transmission_pub_sub_pull_push_server_client(test_case):
    worker = [PatternSendWorker(test_case), PatternReceiveWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


@dataclass(unsafe_hash=True, slots=True)
class PatternsAutoTestCase:
    pattern1: Connection
    pattern2: Connection
    wait1: float
    wait2: float
    data: object
    compression: bool


# Actions for connection bind
# publisher, pusher, pair
class PatternSendAutoWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsAutoTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern1.open()
        sleep(self.test_case.wait1)
        self.result = Transmission.send(self.test_case.pattern1, self.test_case.data, compression=self.test_case.compression)
        sleep(self.test_case.wait1)
        self.test_case.pattern1.close()


# # Actions for connection connect
# # subscriber, puller, pair
class PatternReceiveAutoWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern2.open()
        sleep(self.test_case.wait2)
        self.result = Transmission.recv(self.test_case.pattern2)
        sleep(self.test_case.wait2)
        self.test_case.pattern2.close()


TestCasesAutoPubSubPushPullServerClient = [
    # Publisher/Subscriber Server/Client
    # No Compression
    PatternsAutoTestCase(pattern1=Publisher('PUB', Connection.SERVER, urls=Url.Remote(ip='*'), auto_open=False), wait1=0.4,
                         pattern2=Subscriber('SUB', Connection.CLIENT, urls=Url.Remote(), auto_open=False), wait2=0.4,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Publisher('PUB', Connection.SERVER, urls=Url.Local(), auto_open=False), wait1=0.4,
                         pattern2=Subscriber('SUB', Connection.CLIENT, urls=Url.Local(), auto_open=False), wait2=0.4,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Publisher('PUB', Connection.SERVER, urls=Url.Local(local_type=Url.IPC), auto_open=False), wait1=0.4,
                         pattern2=Subscriber('SUB', Connection.CLIENT, urls=Url.Local(local_type=Url.IPC), auto_open=False), wait2=0.4,
                         data=DATA, compression=False),
    # With Compression
    PatternsAutoTestCase(pattern1=Publisher('PUB', Connection.SERVER, urls=Url.Remote(ip='*'), auto_open=False), wait1=0.4,
                         pattern2=Subscriber('SUB', Connection.CLIENT, urls=Url.Remote(), auto_open=False), wait2=0.4,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Publisher('PUB', Connection.SERVER, urls=Url.Local(), auto_open=False), wait1=0.4,
                         pattern2=Subscriber('SUB', Connection.CLIENT, urls=Url.Local(), auto_open=False), wait2=0.4,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Publisher('PUB', Connection.SERVER, urls=Url.Local(local_type=Url.IPC), auto_open=False), wait1=0.4,
                         pattern2=Subscriber('SUB', Connection.CLIENT, urls=Url.Local(local_type=Url.IPC), auto_open=False), wait2=0.4,
                         data=DATA, compression=False),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesAutoPubSubPushPullServerClient)
def test_transmission_auto_open_pub_sub_pull_push_server_client(test_case):
    worker = [PatternSendAutoWorker(test_case), PatternReceiveAutoWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data
