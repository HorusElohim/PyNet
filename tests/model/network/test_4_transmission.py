from pynet.model.network.transmission import Packet, Transmission, Connection
from pynet.model.network.url import Url, BaseUrl
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
from time import sleep
import pytest

DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


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
    type1: Connection.Type
    type2: Connection.Type
    pattern1: Connection.Pattern
    pattern2: Connection.Pattern
    wait1: float
    wait2: float
    url1: BaseUrl
    url2: BaseUrl
    data: object
    compression: bool


# Actions for connection bind
# publisher, pusher
class TransmissionBindWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.name1, self.test_case.type1, self.test_case.pattern1)
        c.url = self.test_case.url1
        c.open()
        sleep(self.test_case.wait1)
        self.result = Transmission.send(c, self.test_case.data, compression=self.test_case.compression)
        sleep(self.test_case.wait1)
        c.close()


# # Actions for connection connect
# # subscriber, puller
class TransmissionConnectWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.name2, self.test_case.type2, self.test_case.pattern2)
        c.url = self.test_case.url2
        c.open()
        sleep(self.test_case.wait2)
        self.result = Transmission.recv(c)
        sleep(self.test_case.wait2)
        c.close()


TestCasesPubSubPushPullServerClient = [
    # Publisher/Subscriber Server/Client No Compression
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Remote(ip='*'), wait1=0.3,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Remote(), wait2=0.4,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(), wait1=0.3,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(), wait2=0.4,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                          compression=False, data=DATA, )),
    # Publisher/Subscriber Server/Client With Compression
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Remote(ip='*'), wait1=0.3,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Remote(), wait2=0.4,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(), wait1=0.3,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(), wait2=0.4,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                          compression=True, data=DATA, )),

    # Pusher/Puller Server/Client No Compression
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Remote(ip='*'), wait1=0.3,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Remote(), wait2=0.4,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(), wait1=0.3,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(), wait2=0.4,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                          compression=False, data=DATA, )),
    # Pusher/Puller Server/Client With Compression
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Remote(ip='*'), wait1=0.3,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Remote(), wait2=0.4,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(), wait1=0.3,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(), wait2=0.4,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                          compression=True, data=DATA, )),

    # Pair Server/Client No Compression
    (TransmissionTestCase(name1='TestPair', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Remote(ip='*'), wait1=0.3,
                          name2='TestPair', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Remote(), wait2=0.4,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPair', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(), wait1=0.3,
                          name2='TestPair', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(), wait2=0.4,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPair', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                          name2='TestPair', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                          compression=False, data=DATA, )),
    # Pair Server/Client With Compression
    (TransmissionTestCase(name1='TestPair', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Remote(ip='*'), wait1=0.3,
                          name2='TestPair', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Remote(), wait2=0.4,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPair', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(), wait1=0.3,
                          name2='TestPair', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(), wait2=0.4,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPair', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                          name2='TestPair', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                          compression=True, data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesPubSubPushPullServerClient)
def test_transmission_pub_sub_pull_push_server_client(test_case):
    worker = [TransmissionBindWorker(test_case), TransmissionConnectWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


TestCasesPubSubPushPullClientServer = [
    # Publisher/Subscriber Client/Server No Compression
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Remote(ip='*'), wait1=0.4,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Remote(), wait2=0.2,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(), wait1=0.4,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(), wait2=0.2,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                          compression=False, data=DATA, )),
    # Publisher/Subscriber Client/Server With Compression
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Remote(ip='*'), wait1=0.4,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Remote(), wait2=0.2,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(), wait1=0.4,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(), wait2=0.2,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                          name2='TestSUB', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                          compression=True, data=DATA, )),
    # Pusher/Puller Client/Server No Compression
    (TransmissionTestCase(name1='TestPUB', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Remote(ip='*'), wait1=0.4,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Remote(), wait2=0.2,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(), wait1=0.4,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(), wait2=0.2,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                          compression=False, data=DATA, )),
    # Pusher/Puller Client/Server With Compression
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Remote(ip='*'), wait1=0.4,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Remote(), wait2=0.2,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(), wait1=0.4,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(), wait2=0.2,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPUSH', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                          name2='TestPULL', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                          compression=True, data=DATA, )),
    # Pair Client/Server  No Compression
    (TransmissionTestCase(name1='TestPAIR', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Remote(ip='*'), wait1=0.4,
                          name2='TestPAIR', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Remote(), wait2=0.2,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPAIR', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(), wait1=0.4,
                          name2='TestPAIR', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(), wait2=0.2,
                          compression=False, data=DATA, )),
    (TransmissionTestCase(name1='TestPAIR', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                          name2='TestPAIR', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                          compression=False, data=DATA, )),
    # Pair Client/Server  With Compression
    (TransmissionTestCase(name1='TestPAIR', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Remote(ip='*'), wait1=0.4,
                          name2='TestPAIR', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Remote(), wait2=0.2,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPAIR', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(), wait1=0.4,
                          name2='TestPAIR', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(), wait2=0.2,
                          compression=True, data=DATA, )),
    (TransmissionTestCase(name1='TestPAIR', type1=Connection.SERVER, pattern1=Connection.PAIR, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                          name2='TestPAIR', type2=Connection.CLIENT, pattern2=Connection.PAIR, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                          compression=True, data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/Client
@pytest.mark.parametrize('test_case', TestCasesPubSubPushPullClientServer)
def test_transmission_pub_sub_pull_push_client_server(test_case):
    worker = [TransmissionConnectWorker(test_case), TransmissionBindWorker(test_case)]
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
        c = Connection(self.test_case.name1, self.test_case.type1, self.test_case.pattern1)
        c.url = self.test_case.url1
        c.open()
        sleep(self.test_case.wait1)
        req = Transmission.recv(c)
        rep = Transmission.send(c, self.test_case.data, compression=self.test_case.compression)
        c.close()
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
        c = Connection(self.test_case.name2, self.test_case.type2, self.test_case.pattern2)
        c.url = self.test_case.url2
        c.open()
        sleep(self.test_case.wait2)
        req_res = Transmission.send(c, self.test_case.data, compression=self.test_case.compression)
        rep = Transmission.recv(c)
        sleep(self.test_case.wait2)
        c.close()
        self.result = {
            'req_result': req_res,
            'rep': rep
        }


TestCasesReqRepServerClient = [
    TransmissionTestCase(name1='TestREP', type1=Connection.SERVER, pattern1=Connection.REP, url1=Url.Remote(ip='*'), wait1=0.4,
                         name2='TestREQ', type2=Connection.CLIENT, pattern2=Connection.REQ, url2=Url.Remote(), wait2=0.2,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', type1=Connection.SERVER, pattern1=Connection.REP, url1=Url.Local(), wait1=0.4,
                         name2='TestREQ', type2=Connection.CLIENT, pattern2=Connection.REQ, url2=Url.Local(), wait2=0.2,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', type1=Connection.SERVER, pattern1=Connection.REP, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                         name2='TestREQ', type2=Connection.CLIENT, pattern2=Connection.REQ, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', type1=Connection.SERVER, pattern1=Connection.REP, url1=Url.Remote(ip='*'), wait1=0.4,
                         name2='TestREQ', type2=Connection.CLIENT, pattern2=Connection.REQ, url2=Url.Remote(), wait2=0.2,
                         data=DATA, compression=True),
    TransmissionTestCase(name1='TestREP', type1=Connection.SERVER, pattern1=Connection.REP, url1=Url.Local(), wait1=0.4,
                         name2='TestREQ', type2=Connection.CLIENT, pattern2=Connection.REQ, url2=Url.Local(), wait2=0.2,
                         data=DATA, compression=True),
    TransmissionTestCase(name1='TestREP', type1=Connection.SERVER, pattern1=Connection.REP, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                         name2='TestREQ', type2=Connection.CLIENT, pattern2=Connection.REQ, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                         data=DATA, compression=True),

]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case', TestCasesReqRepServerClient)
def test_connections_req_rep_server_client(test_case):
    workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['req'] == test_case.data
    assert workers[0].result['rep_result']

    assert workers[1].result['rep'] == test_case.data
    assert workers[1].result['req_result']


TestCasesReqRepClientServer = [
    TransmissionTestCase(name1='TestREP', type1=Connection.CLIENT, pattern1=Connection.REP, url1=Url.Remote(), wait1=0.2,
                         name2='TestREQ', type2=Connection.SERVER, pattern2=Connection.REQ, url2=Url.Remote(ip='*'), wait2=0.4,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', type1=Connection.CLIENT, pattern1=Connection.REP, url1=Url.Local(), wait1=0.2,
                         name2='TestREQ', type2=Connection.SERVER, pattern2=Connection.REQ, url2=Url.Local(), wait2=0.4,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', type1=Connection.CLIENT, pattern1=Connection.REP, url1=Url.Local(local_type=Url.IPC), wait1=0.2,
                         name2='TestREQ', type2=Connection.SERVER, pattern2=Connection.REQ, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                         data=DATA, compression=False),
    TransmissionTestCase(name1='TestREP', type1=Connection.CLIENT, pattern1=Connection.REP, url1=Url.Remote(), wait1=0.2,
                         name2='TestREQ', type2=Connection.SERVER, pattern2=Connection.REQ, url2=Url.Remote(ip='*'), wait2=0.4,
                         data=DATA, compression=True),
    TransmissionTestCase(name1='TestREP', type1=Connection.CLIENT, pattern1=Connection.REP, url1=Url.Local(), wait1=0.2,
                         name2='TestREQ', type2=Connection.SERVER, pattern2=Connection.REQ, url2=Url.Local(), wait2=0.4,
                         data=DATA, compression=True),
    TransmissionTestCase(name1='TestREP', type1=Connection.CLIENT, pattern1=Connection.REP, url1=Url.Local(local_type=Url.IPC), wait1=0.2,
                         name2='TestREQ', type2=Connection.SERVER, pattern2=Connection.REQ, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                         data=DATA, compression=True),

]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case', TestCasesReqRepClientServer)
def test_connections_req_rep_client_server(test_case):
    workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['req'] == test_case.data
    assert workers[0].result['rep_result']

    assert workers[1].result['rep'] == test_case.data
    assert workers[1].result['req_result']
