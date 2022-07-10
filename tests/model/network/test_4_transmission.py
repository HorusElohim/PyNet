from pynet.model.network.transmission import Transmission
from pynet.model.network.sock import Sock
from pynet.model import Logger
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
from time import sleep
import pytest
import os

DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]

TEST_LOG = Logger('test_4_transmission')


def test_transmission_packets():
    pkt = Transmission.to_packet('ConnectionName', DATA)
    assert pkt.encoded
    data = Transmission.from_packet(pkt)
    assert not pkt.encoded
    assert data == DATA


def test_transmission_compressed_packets():
    pkt = Transmission.to_packet('ConnectionName', DATA, compression=True)
    assert pkt.compressed
    data = Transmission.from_packet(pkt)
    assert not pkt.compressed
    assert data == DATA


@dataclass(unsafe_hash=True, slots=True)
class TransmissionTestCase:
    name1: str
    name2: str
    pattern1: Sock.Pattern
    pattern2: Sock.Pattern
    wait1: float
    wait2: float
    url1: Sock.SockUrl
    url2: Sock.SockUrl
    data: object
    compression: bool


# Actions for connection bind
# publisher, pusher
class TransmissionSendWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name1, self.test_case.pattern1, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url1
        sock.open()
        sleep(self.test_case.wait1)
        self.result = Transmission.send(sock, self.test_case.data, compression=self.test_case.compression)
        sleep(self.test_case.wait1)
        sock.close()


# # Actions for connection connect
# # subscriber, puller
class TransmissionReceiveWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Sock(self.test_case.name2, self.test_case.pattern2, logger_other=TEST_LOG)
        c.sock_urls = self.test_case.url2
        c.open()
        sleep(self.test_case.wait2)
        self.result = Transmission.recv(c)
        sleep(self.test_case.wait2)
        c.close()


if os.name != 'nt':
    TestCasesPubSubPushPullServerClientLocal = [
        # Publisher/Subscriber Server/Client No Compression
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                              compression=False, data=DATA, )),
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait1=0.3,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait2=0.4, compression=False, data=DATA, )),
        # Publisher/Subscriber Server/Client With Compression
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                              compression=True, data=DATA, )),
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait1=0.3,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait2=0.4,
                              compression=True, data=DATA, )),

        # Pusher/Puller Server/Client No Compression
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                              compression=False, data=DATA, )),
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait1=0.3,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait2=0.4,
                              compression=False, data=DATA, )),
        # Pusher/Puller Server/Client With Compression
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                              compression=True, data=DATA, )),
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait1=0.3,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait2=0.4,
                              compression=True, data=DATA, )),

        # Pair Server/Client No Compression
        (TransmissionTestCase(name1='TestPair', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                              name2='TestPair', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                              compression=False, data=DATA, )),
        (TransmissionTestCase(name1='TestPair', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait1=0.3,
                              name2='TestPair', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait2=0.4,
                              compression=False, data=DATA, )),
        # Pair Server/Client With Compression
        (TransmissionTestCase(name1='TestPair', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                              name2='TestPair', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                              compression=True, data=DATA, )),
        (TransmissionTestCase(name1='TestPair', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait1=0.3,
                              name2='TestPair', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait2=0.4,
                              compression=True, data=DATA, )),
    ]


    # Test Publisher/Subscriber
    # Test Pusher/Puller
    # Server/Client
    @pytest.mark.parametrize('test_case', TestCasesPubSubPushPullServerClientLocal)
    def test_transmission_pub_sub_pull_push_server_client_local(test_case):
        worker = [TransmissionSendWorker(test_case), TransmissionReceiveWorker(test_case)]
        WorkerRunner.run(worker)
        assert worker[0].result
        assert worker[1].result == test_case.data

TestCasesPubSubPushPullServerClientRemote = [
    # Publisher/Subscriber Server/Client No Compression
    (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                          name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                          compression=False, data=DATA, )),
    # Publisher/Subscriber Server/Client With Compression
    (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                          name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                          compression=True, data=DATA, )),

    # Pusher/Puller Server/Client No Compression
    (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                          name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                          compression=False, data=DATA, )),
    # Pusher/Puller Server/Client With Compression
    (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                          name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                          compression=True, data=DATA, )),

    # Pair Server/Client No Compression
    (TransmissionTestCase(name1='TestPair', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                          name2='TestPair', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                          compression=False, data=DATA, )),
    # Pair Server/Client With Compression
    (TransmissionTestCase(name1='TestPair', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                          name2='TestPair', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                          compression=True, data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesPubSubPushPullServerClientRemote)
def test_transmission_pub_sub_pull_push_server_client_remote(test_case):
    worker = [TransmissionSendWorker(test_case), TransmissionReceiveWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


if os.name != 'nt':
    TestCasesPubSubPushPullClientServerLocal = [
        # Publisher/Subscriber Client/Server No Compression
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.5,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.1,
                              compression=False, data=DATA, )),
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait1=0.5,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait2=0.1,
                              compression=False, data=DATA, )),
        # Publisher/Subscriber Client/Server With Compression
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.5,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.1,
                              compression=True, data=DATA, )),
        (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait1=0.5,
                              name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait2=0.1,
                              compression=True, data=DATA, )),
        # Pusher/Puller Client/Server No Compression
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.5,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.1,
                              compression=False, data=DATA, )),
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait1=0.5,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait2=0.1,
                              compression=False, data=DATA, )),
        # Pusher/Puller Client/Server With Compression
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.5,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.1,
                              compression=True, data=DATA, )),
        (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait1=0.5,
                              name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait2=0.1,
                              compression=True, data=DATA, )),
        # Pair Client/Server  No Compression
        (TransmissionTestCase(name1='TestPAIR', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.5,
                              name2='TestPAIR', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.1,
                              compression=False, data=DATA, )),
        (TransmissionTestCase(name1='TestPAIR', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait1=0.5,
                              name2='TestPAIR', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait2=0.1,
                              compression=False, data=DATA, )),
        # Pair Client/Server  With Compression
        (TransmissionTestCase(name1='TestPAIR', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.5,
                              name2='TestPAIR', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.1,
                              compression=True, data=DATA, )),
        (TransmissionTestCase(name1='TestPAIR', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                              wait1=0.5,
                              name2='TestPAIR', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                              wait2=0.1,
                              compression=True, data=DATA, )),
    ]


    # Test Publisher/Subscriber
    # Test Pusher/Puller
    # Server/Client
    @pytest.mark.parametrize('test_case', TestCasesPubSubPushPullClientServerLocal)
    def test_transmission_pub_sub_pull_push_client_server_local(test_case):
        worker = [TransmissionReceiveWorker(test_case), TransmissionSendWorker(test_case)]
        WorkerRunner.run(worker)
        assert worker[1].result
        assert worker[0].result == test_case.data

TestCasesPubSubPushPullClientServerRemote = [
    # Publisher/Subscriber Client/Server No Compression
    (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.5,
                          name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip="*"), wait2=0.1,
                          compression=False, data=DATA, )),
    # Publisher/Subscriber Client/Server With Compression
    (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.5,
                          name2='TestSUB', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.1,
                          compression=True, data=DATA, )),
    # Pusher/Puller Client/Server No Compression
    (TransmissionTestCase(name1='TestPUB', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.5,
                          name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.1,
                          compression=False, data=DATA, )),
    # Pusher/Puller Client/Server With Compression
    (TransmissionTestCase(name1='TestPUSH', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.5,
                          name2='TestPULL', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.1,
                          compression=True, data=DATA, )),
    # Pair Client/Server  No Compression
    (TransmissionTestCase(name1='TestPAIR', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.5,
                          name2='TestPAIR', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.1,
                          compression=False, data=DATA, )),
    # Pair Client/Server  With Compression
    (TransmissionTestCase(name1='TestPAIR', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.5,
                          name2='TestPAIR', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.1,
                          compression=True, data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesPubSubPushPullClientServerRemote)
def test_transmission_pub_sub_pull_push_client_server_remote(test_case):
    worker = [TransmissionReceiveWorker(test_case), TransmissionSendWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[1].result
    assert worker[0].result == test_case.data


# Actions for connection bind
# replier
class TransmissionReplierWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name1, self.test_case.pattern1, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url1
        sock.open()
        sleep(self.test_case.wait1)
        req = Transmission.recv(sock)
        rep = Transmission.send(sock, self.test_case.data, compression=self.test_case.compression)
        sock.close()
        self.result = {
            'req': req,
            'rep_result': rep
        }


# # # Actions for connection connect
# # requester
class TransmissionRequesterWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name2, self.test_case.pattern2, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url2
        sock.open()
        sleep(self.test_case.wait2)
        req_res = Transmission.send(sock, self.test_case.data, compression=self.test_case.compression)
        rep = Transmission.recv(sock)
        sleep(self.test_case.wait2)
        sock.close()
        self.result = {
            'req_result': req_res,
            'rep': rep
        }


if os.name != 'nt':
    TestCasesReqRepServerClientLocal = [
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.4,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.2,
                             data=DATA, compression=False),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                             wait1=0.4,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                             wait2=0.2,
                             data=DATA, compression=False),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.4,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.2,
                             data=DATA, compression=True),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                             wait1=0.4,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                             wait2=0.2,
                             data=DATA, compression=True),

    ]


    # Test Publisher/Subscriber
    # Test Pusher/Puller
    @pytest.mark.parametrize('test_case', TestCasesReqRepServerClientLocal)
    def test_connections_req_rep_server_client_local(test_case):
        workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
        WorkerRunner.run(workers)
        assert workers[0].result
        assert workers[1].result

        assert workers[0].result['req'] == test_case.data
        assert workers[0].result['rep_result']

        assert workers[1].result['rep'] == test_case.data
        assert workers[1].result['req_result']

TestCasesReqRepServerClientRemote = [
    TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.4,
                         name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.2,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.4,
                         name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.2,
                         data=DATA, compression=True),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case', TestCasesReqRepServerClientRemote)
def test_connections_req_rep_server_client_remote(test_case):
    workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['req'] == test_case.data
    assert workers[0].result['rep_result']

    assert workers[1].result['rep'] == test_case.data
    assert workers[1].result['req_result']


if os.name != 'nt':
    TestCasesReqRepClientServerLocal = [
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.2,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.4,
                             data=DATA, compression=False),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                             wait1=0.2,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                             wait2=0.4,
                             data=DATA, compression=False),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.2,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.4,
                             data=DATA, compression=True),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.2,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.4,
                             data=DATA, compression=True),
        TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                             wait1=0.2,
                             name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                             wait2=0.4,
                             data=DATA, compression=True),

    ]


    # Test Publisher/Subscriber
    # Test Pusher/Puller
    @pytest.mark.parametrize('test_case', TestCasesReqRepClientServerLocal)
    def test_connections_req_rep_client_server_local(test_case):
        workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
        WorkerRunner.run(workers)
        assert workers[0].result
        assert workers[1].result

        assert workers[0].result['req'] == test_case.data
        assert workers[0].result['rep_result']

        assert workers[1].result['rep'] == test_case.data
        assert workers[1].result['req_result']

TestCasesReqRepClientServerRemote = [
    TransmissionTestCase(name1='TestREP', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.2,
                         name2='TestREQ', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.4,
                         data=DATA, compression=False),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case', TestCasesReqRepClientServerRemote)
def test_connections_req_rep_client_server_remote(test_case):
    workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['req'] == test_case.data
    assert workers[0].result['rep_result']

    assert workers[1].result['rep'] == test_case.data
    assert workers[1].result['req_result']
