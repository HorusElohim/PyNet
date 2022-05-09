from pynet.model.network.transmission import Packet, Transmission, Connection
from pynet.model.network.core import CoreType
from pynet.model.network.url import Url, BaseUrl
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
import pytest
import time


def usleep(microsecond):
    time.sleep(microsecond / 1000000.0)


DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_transmission_packets():
    c = Connection('Transmission', CoreType.publisher, Url.Local())
    pkt = Transmission.to_packet(c, DATA)
    assert pkt.encoded
    data = Transmission.from_packet(pkt)
    assert not pkt.encoded
    assert data == DATA


def test_transmission_compressed_packets():
    c = Connection('Transmission', CoreType.publisher, Url.Local())
    pkt = Transmission.to_packet(c, DATA, compression=True)
    assert pkt.compressed
    data = Transmission.from_packet(pkt)
    assert not pkt.compressed
    assert data == DATA


@dataclass(unsafe_hash=True, slots=True)
class TransmissionTestCase:
    c1_name: str
    c2_name: str
    c1_type: CoreType
    c2_type: CoreType
    channel: BaseUrl
    compression: bool
    data: object


@dataclass(unsafe_hash=True, slots=True)
class TC:
    name1: str
    name2: str
    type1: Connection.Type
    type2: Connection.Type
    url: Url.BaseUrl
    compression: bool
    data: object


# Actions for connection bind
# publisher, pusher
class TransmissionBindWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c1_name, self.test_case.c1_type, self.test_case.channel)
        c.open()
        usleep(5000)
        self.result = Transmission.send(c, self.test_case.data, compression=self.test_case.compression)
        c.close()


# # Actions for connection connect
# # subscriber, puller
class TransmissionConnectWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c2_name, self.test_case.c2_type, self.test_case.channel)
        c.open()
        self.result = Transmission.recv(c)
        c.close()


Transmission_pub_sub_push_pull = [
    TC(name1='PUB', type1=Connection.SERVER, name2='SUB', type2=Connection.CLIENT, url=Url.Remote(), data=DATA, compression=False),
    TC(name1='PUB', type1=Connection.CLIENT, name2='SUB', type2=Connection.SERVER, url=Url.Remote(), data=DATA, compression=False)
]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Url.Remote(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Url.Local(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Url.Local(local_type=Url.LocalType().ipc),
                                                   compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Url.Remote(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Url.Local(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Url.Local(local_type=Url.LocalType().ipc),
                                                   compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Url.Remote(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Url.Local(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Url.Local(local_type=Url.LocalType().ipc),
                                                   compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Url.Remote(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Url.Local(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Url.Local(local_type=Url.LocalType().ipc),
                                                   compression=True, data=DATA, )),
                         ])
def test_transmission_pub_sub_pull_push(test_case):
    worker = [TransmissionBindWorker(test_case), TransmissionConnectWorker(test_case)]
    WorkerRunner.run(worker)
    assert worker[0].result
    assert worker[1].result == test_case.data


# Actions for connection bind
# replier
class TransmissionReplierWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c1_name, self.test_case.c1_type, self.test_case.channel)
        c.open()
        req = Transmission.recv(c)
        usleep(5000)
        rep = Transmission.send(c, self.test_case.data, compression=self.test_case.compression)
        c.close()
        self.result = {
            'req': req,
            'rep_result': rep
        }


# # Actions for connection connect
# requester
class TransmissionRequesterWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: TransmissionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c2_name, self.test_case.c2_type, self.test_case.channel)
        c.open()
        usleep(5000)
        req_res = Transmission.send(c, self.test_case.data, compression=self.test_case.compression)
        rep = Transmission.recv(c)
        c.close()
        self.result = {
            'req_result': req_res,
            'rep': rep
        }


# Actions for connection bind
# replier
def thread_connection_replier(test_case: TransmissionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    req = Transmission.recv(c)
    usleep(5000)
    rep = Transmission.send(c, test_case.data, compression=test_case.compression)
    c.close()
    return {
        'req': req,
        'rep_result': rep
    }


#
# Actions for connection connect
# requester
def thread_connection_requester(test_case: TransmissionTestCase):
    c = Connection(test_case.c2_name, test_case.c2_type, test_case.channel)
    c.open()
    usleep(5000)
    req_res = Transmission.send(c, test_case.data, compression=test_case.compression)
    rep = Transmission.recv(c)
    c.close()
    return {
        'req_result': req_res,
        'rep': rep
    }


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (TransmissionTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                                   c2_name='TestRequester', c2_type=CoreType.requester,
                                                   channel=Url.Remote(),
                                                   data=DATA, compression=False)),
                             (TransmissionTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                                   c2_name='TestRequester', c2_type=CoreType.requester,
                                                   channel=Url.Local(),
                                                   data=DATA, compression=False)),
                             (TransmissionTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                                   c2_name='TestRequester', c2_type=CoreType.requester,
                                                   channel=Url.Local(local_type=Url.LocalType().inproc),
                                                   data=DATA, compression=False)),
                             (TransmissionTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                                   c2_name='TestRequester', c2_type=CoreType.requester,
                                                   channel=Url.Remote(),
                                                   data=DATA, compression=True)),
                             (TransmissionTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                                   c2_name='TestRequester', c2_type=CoreType.requester,
                                                   channel=Url.Local(),
                                                   data=DATA, compression=True)),
                             (TransmissionTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                                   c2_name='TestRequester', c2_type=CoreType.requester,
                                                   channel=Url.Local(local_type=Url.LocalType().inproc),
                                                   data=DATA, compression=True)),
                         ])
def test_connections_req_rep(test_case):
    workers = [TransmissionReplierWorker(test_case), TransmissionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['req'] == test_case.data
    assert workers[0].result['rep_result']

    assert workers[1].result['rep'] == test_case.data
    assert workers[1].result['req_result']
