from pynet.model.network.connection import Connection
from pynet.model.network.core import CoreType
from dataclassy import dataclass
from pynet.model.network.url import Url, BaseUrl
from .thread_runner import Worker, WorkerRunner
import pytest
import time


def usleep(microsecond):
    time.sleep(microsecond / 1000000.0)


# DATA = [1, 2, 3, 4, 6, 8, 9]
DATA = "TestData"


# _______ ConnectionBase Section _______

@pytest.mark.parametrize(
    'connection_type, channel_type',
    [
        (CoreType.publisher, Url.Local(local_type=Url.LocalType().ipc)),
        (CoreType.subscriber, Url.Local(local_type=Url.LocalType().ipc)),
        (CoreType.puller, Url.Local(local_type=Url.LocalType().ipc)),
        (CoreType.pusher, Url.Local(local_type=Url.LocalType().ipc)),
        (CoreType.replier, Url.Local(local_type=Url.LocalType().ipc)),
        (CoreType.requester, Url.Local(local_type=Url.LocalType().ipc)),

        (CoreType.publisher, Url.Local(local_type=Url.LocalType().inproc)),
        (CoreType.subscriber, Url.Local(local_type=Url.LocalType().inproc)),
        (CoreType.puller, Url.Local(local_type=Url.LocalType().inproc)),
        (CoreType.pusher, Url.Local(local_type=Url.LocalType().inproc)),
        (CoreType.replier, Url.Local(local_type=Url.LocalType().inproc)),
        (CoreType.requester, Url.Local(local_type=Url.LocalType().inproc)),

        (CoreType.publisher, Url.Remote(port=28128)),
        (CoreType.subscriber, Url.Remote(port=28128)),
        (CoreType.puller, Url.Remote(port=28129)),
        (CoreType.pusher, Url.Remote(port=28129)),
        (CoreType.replier, Url.Remote(port=28130)),
        (CoreType.requester, Url.Remote(port=28130)),

    ])
def test_connection_creation(connection_type, channel_type):
    c = Connection('TestConnectionCreation', connection_type, channel_type)
    assert c is not None
    c.open()
    assert c.is_open()
    assert c.url == channel_type
    assert c.core_type == connection_type
    c.close()
    assert not c.is_open()


@dataclass(unsafe_hash=True, slots=True)
class ConnectionTestCase:
    c1_name: str
    c2_name: str
    c1_type: CoreType
    c2_type: CoreType
    channel: BaseUrl
    data: object


# Actions for connection bind
# publisher, pusher
class ConnectionBindWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c1_name, self.test_case.c1_type, self.test_case.channel)
        c.open()
        usleep(5000)
        self.result = c.send(str(self.test_case.data).encode("utf-8"))
        c.close()


# # Actions for connection connect
# # subscriber, puller
class ConnectionConnectWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c2_name, self.test_case.c2_type, self.test_case.channel)
        c.open()
        self.result = c.recv()
        c.close()


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                 c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                 channel=Url.Remote(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                 c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                 channel=Url.Local(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                 c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                 channel=Url.Local(local_type=Url.LocalType().ipc),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                 c2_name='TestPuller', c2_type=CoreType.puller,
                                                 channel=Url.Remote(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                 c2_name='TestPuller', c2_type=CoreType.puller,
                                                 channel=Url.Local(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                 c2_name='TestPuller', c2_type=CoreType.puller,
                                                 channel=Url.Local(local_type=Url.LocalType().ipc),
                                                 data=DATA, )),
                         ])
def test_connections_pub_sub_pull_push(test_case):
    workers = [ConnectionBindWorker(test_case), ConnectionConnectWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert bytes(workers[1].result).decode('utf-8') == test_case.data


# Test Requester/Replier

# Actions for connection bind
# publisher, pusher
class ConnectionReplierWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c1_name, self.test_case.c1_type, self.test_case.channel)
        c.open()
        req = c.recv()
        usleep(5000)
        rep = c.send(str(self.test_case.data).encode("utf-8"))
        c.close()
        self.result = {
            'req': req,
            'rep_result': rep
        }


def thread_connection_replier(test_case: ConnectionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    req = c.recv()
    usleep(5000)
    rep = c.send(str(test_case.data).encode("utf-8"))
    c.close()
    return {
        'req': req,
        'rep_result': rep
    }


#
# # Actions for connection connect
# # subscriber, puller
class ConnectionRequesterWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.c2_name, self.test_case.c2_type, self.test_case.channel)
        c.open()
        usleep(5000)
        req_res = c.send(str(self.test_case.data).encode("utf-8"))
        rep = c.recv()
        c.close()
        self.result = {
            'req_result': req_res,
            'rep': rep
        }


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.replier,
                                                 c2_name='TestSubscriber', c2_type=CoreType.requester,
                                                 channel=Url.Remote(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.replier,
                                                 c2_name='TestSubscriber', c2_type=CoreType.requester,
                                                 channel=Url.Local(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.replier,
                                                 c2_name='TestSubscriber', c2_type=CoreType.requester,
                                                 channel=Url.Local(local_type=Url.LocalType().inproc),
                                                 data=DATA, )),
                         ])
def test_connections_req_rep(test_case):
    workers = [ConnectionReplierWorker(test_case), ConnectionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0]
    assert workers[1]

    assert workers[0].result['rep_result']
    assert bytes(workers[0].result['req']).decode("utf-8") == test_case.data

    assert workers[1].result['req_result']
    assert bytes(workers[1].result['rep']).decode("utf-8") == test_case.data
