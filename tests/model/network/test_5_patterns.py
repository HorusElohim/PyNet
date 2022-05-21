from pynet.model import Logger
from pynet.model.network import Sock
from pynet.model.network.patterns import *
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
from time import sleep
import pytest

DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]

TEST_LOG = Logger('test_5_patterns')


@dataclass(unsafe_hash=True, slots=True)
class PatternsTestCase:
    pattern1: PatternBase
    pattern2: PatternBase
    wait1: float
    wait2: float
    url1: Sock.SockUrl
    url2: Sock.SockUrl
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
        self.test_case.pattern1.sock_urls = self.test_case.url1
        self.test_case.pattern1.open()
        sleep(self.test_case.wait1)
        self.result = self.test_case.pattern1.send(self.test_case.data, self.test_case.compression)
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
        self.test_case.pattern2.sock_urls = self.test_case.url2
        self.test_case.pattern2.open()
        sleep(self.test_case.wait2)
        self.result = self.test_case.pattern2.receive()
        sleep(self.test_case.wait2)
        self.test_case.pattern2.close()


TestCasesPubSubPushPullServerClient = [
    # Publisher/Subscriber Server/Client
    # No Compression
    PatternsTestCase(pattern1=Publisher('PUB', logger_other=TEST_LOG), wait1=0.4, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'),
                     pattern2=Subscriber('SUB', logger_other=TEST_LOG), wait2=0.4, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT),
                     data=DATA, compression=False),
    PatternsTestCase(pattern1=Publisher('PUB', logger_other=TEST_LOG), wait1=0.4, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER),
                     pattern2=Subscriber('SUB', logger_other=TEST_LOG), wait2=0.4, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT),
                     data=DATA, compression=False),
    PatternsTestCase(pattern1=Publisher('PUB', logger_other=TEST_LOG), wait1=0.4, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                     pattern2=Subscriber('SUB', logger_other=TEST_LOG), wait2=0.4, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                     data=DATA, compression=False),
    # With Compression
    PatternsTestCase(pattern1=Publisher('PUB', logger_other=TEST_LOG), wait1=0.4, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'),
                     pattern2=Subscriber('SUB', logger_other=TEST_LOG), wait2=0.4, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT),
                     data=DATA, compression=True),
    PatternsTestCase(pattern1=Publisher('PUB', logger_other=TEST_LOG), wait1=0.4, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER),
                     pattern2=Subscriber('SUB', logger_other=TEST_LOG), wait2=0.4, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT),
                     data=DATA, compression=True),
    PatternsTestCase(pattern1=Publisher('PUB', logger_other=TEST_LOG), wait1=0.4, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                     pattern2=Subscriber('SUB', logger_other=TEST_LOG), wait2=0.4, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
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


#

@dataclass(unsafe_hash=True, slots=True)
class PatternsAutoTestCase:
    pattern1: PatternBase
    pattern2: PatternBase
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
        self.result = self.test_case.pattern1.send(self.test_case.data, self.test_case.compression)
        sleep(self.test_case.wait1)
        self.test_case.pattern1.close()


# # Actions for connection connect
# # subscriber, puller, pair
class PatternReceiveAutoWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsAutoTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern2.open()
        sleep(self.test_case.wait2)
        self.result = self.test_case.pattern2.receive()
        sleep(self.test_case.wait2)
        self.test_case.pattern2.close()


TestCasesAutoPubSubServerClient = [
    # Publisher/Subscriber Server/Client
    # No Compression
    PatternsAutoTestCase(pattern1=Publisher('PUB', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), auto_open=False, logger_other=TEST_LOG), wait1=0.4,
                         pattern2=Subscriber('SUB', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), auto_open=False, logger_other=TEST_LOG), wait2=0.4,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Publisher('PUB', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER), auto_open=False, logger_other=TEST_LOG), wait1=0.4,
                         pattern2=Subscriber('SUB', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), auto_open=False, logger_other=TEST_LOG), wait2=0.4,
                         data=DATA, compression=False),
    PatternsAutoTestCase(
        pattern1=Publisher('PUB', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), auto_open=False, logger_other=TEST_LOG), wait1=0.4,
        pattern2=Subscriber('SUB', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), auto_open=False, logger_other=TEST_LOG),
        wait2=0.4,
        data=DATA, compression=False),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesAutoPubSubServerClient)
def test_transmission_auto_open_pub_sub_server_client(test_case):
    worker = [PatternSendAutoWorker(test_case), PatternReceiveAutoWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


TestCasesAutoPushPullServerClient = [
    # Pusher/Puller Server/Client
    # No Compression
    PatternsAutoTestCase(pattern1=Pusher('PUSH', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), auto_open=False, logger_other=TEST_LOG), wait1=0.6,
                         pattern2=Puller('PULL', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), auto_open=False, logger_other=TEST_LOG), wait2=0.2,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Pusher('PUSH', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER), auto_open=False, logger_other=TEST_LOG), wait1=0.6,
                         pattern2=Puller('PULL', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), auto_open=False, logger_other=TEST_LOG), wait2=0.2,
                         data=DATA, compression=False),
    PatternsAutoTestCase(
        pattern1=Pusher('PUSH', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), auto_open=False, logger_other=TEST_LOG), wait1=0.6,
        pattern2=Puller('PULL', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), auto_open=False, logger_other=TEST_LOG), wait2=0.1,
        data=DATA, compression=False),
    # With Compression
    PatternsAutoTestCase(pattern1=Pusher('PUSH', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*', port=28129), auto_open=False, logger_other=TEST_LOG),
                         wait1=0.6,
                         pattern2=Puller('PULL', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT, port=28129), auto_open=False, logger_other=TEST_LOG), wait2=0.2,
                         data=DATA, compression=True),
    PatternsAutoTestCase(pattern1=Pusher('PUSH', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, path='/tmp/pynet_1'), auto_open=False, logger_other=TEST_LOG),
                         wait1=0.6,
                         pattern2=Puller('PULL', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, path='/tmp/pynet_1'), auto_open=False, logger_other=TEST_LOG),
                         wait2=0.2,
                         data=DATA, compression=True),
    PatternsAutoTestCase(
        pattern1=Pusher('PUSH', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, path='/tmp/pynet_2', local_type=Sock.SockUrl.IPC), auto_open=False,
                        logger_other=TEST_LOG),
        wait1=0.9,
        pattern2=Puller('PULL', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, path='/tmp/pynet_2', local_type=Sock.SockUrl.IPC), auto_open=False,
                        logger_other=TEST_LOG),
        wait2=0.2,
        data=DATA, compression=True),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesAutoPushPullServerClient)
def test_transmission_auto_open_push_pull_server_client(test_case):
    worker = [PatternSendAutoWorker(test_case), PatternReceiveAutoWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


TestCasesAutoPairServerClient = [
    # Pair
    # No Compression
    PatternsAutoTestCase(pattern1=Pair('PAIR1', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), auto_open=False, logger_other=TEST_LOG), wait1=0.4,
                         pattern2=Pair('PAIR2', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), auto_open=False, logger_other=TEST_LOG), wait2=0.3,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Pair('PAIR1', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, path='/tmp/pynet_1'), auto_open=False, logger_other=TEST_LOG),
                         wait1=0.4,
                         pattern2=Pair('PAIR2', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, path='/tmp/pynet_1'), auto_open=False, logger_other=TEST_LOG),
                         wait2=0.3,
                         data=DATA, compression=False),
    PatternsAutoTestCase(
        pattern1=Pair('PAIR1', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), auto_open=False, logger_other=TEST_LOG), wait1=0.4,
        pattern2=Pair('PAIR2', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), auto_open=False, logger_other=TEST_LOG), wait2=0.3,
        data=DATA, compression=False),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesAutoPairServerClient)
def test_transmission_auto_open_pair_server_client(test_case):
    worker = [PatternSendAutoWorker(test_case), PatternReceiveAutoWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


# Actions for connection bind
# replier
class PatternReplierWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsAutoTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern1.open()
        sleep(self.test_case.wait1)
        req = self.test_case.pattern1.receive()
        rep = self.test_case.pattern1.send(self.test_case.data, compression=self.test_case.compression)
        sleep(self.test_case.wait1)
        self.test_case.pattern1.close()

        self.result = {
            'req': req,
            'rep_result': rep
        }


# # # Actions for connection connect
# # requester
class PatternRequesterWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: PatternsAutoTestCase = test_case
        self.result = None

    def run(self) -> None:
        self.test_case.pattern1.open()
        sleep(self.test_case.wait1)
        req_res = self.test_case.pattern1.send(self.test_case.data, compression=self.test_case.compression)
        rep = self.test_case.pattern1.receive()
        sleep(self.test_case.wait1)
        self.test_case.pattern1.close()

        self.result = {
            'req_result': req_res,
            'rep': rep
        }


TestCasesAutoPairReqRep = [
    # Pair
    # No Compression
    PatternsAutoTestCase(pattern1=Pair('PAIR1', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), auto_open=False, logger_other=TEST_LOG), wait1=0.4,
                         pattern2=Pair('PAIR2', sock_urls=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), auto_open=False, logger_other=TEST_LOG), wait2=0.3,
                         data=DATA, compression=False),
    PatternsAutoTestCase(pattern1=Pair('PAIR1', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, path='/tmp/pynet_1'), auto_open=False, logger_other=TEST_LOG),
                         wait1=0.4,
                         pattern2=Pair('PAIR2', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, path='/tmp/pynet_1'), auto_open=False, logger_other=TEST_LOG),
                         wait2=0.3,
                         data=DATA, compression=False),
    PatternsAutoTestCase(
        pattern1=Pair('PAIR1', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.SERVER, path='/tmp/pynet_2', local_type=Sock.SockUrl.IPC), auto_open=False,
                      logger_other=TEST_LOG),
        wait1=0.4,
        pattern2=Pair('PAIR2', sock_urls=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, path='/tmp/pynet_2', local_type=Sock.SockUrl.IPC), auto_open=False,
                      logger_other=TEST_LOG),
        wait2=0.3,
        data=DATA, compression=False),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesAutoPairReqRep)
def test_transmission_auto_open_pair_server_client(test_case):
    worker = [PatternSendAutoWorker(test_case), PatternReceiveAutoWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data
