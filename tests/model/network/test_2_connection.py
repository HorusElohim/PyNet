from pynet.model.network.connection import Connection
from dataclassy import dataclass
from pynet.model.network.url import Url, BaseUrl
from .thread_runner import Worker, WorkerRunner
import pytest
from time import sleep

# DATA = [1, 2, 3, 4, 6, 8, 9]
DATA = "TestData"


@dataclass(unsafe_hash=True, slots=True)
class ConnectionTestCase:
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


# Actions for connection bind
# publisher, pusher
class ConnectionSenderWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.name1, self.test_case.type1, self.test_case.pattern1)
        c.url = self.test_case.url1
        c.open()
        sleep(self.test_case.wait1)
        self.result = c.send(str(self.test_case.data).encode("utf-8"))
        sleep(self.test_case.wait1)
        c.close()


# # Actions for connection connect
# # subscriber, puller
class ConnectionReceiverWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.name2, self.test_case.type2, self.test_case.pattern2)
        c.url = self.test_case.url2
        c.open()
        sleep(self.test_case.wait2)
        self.result = c.recv()
        c.close()


TestCaseConnectionsServerClient = [
    # Publisher / Subscribers - Server/Client
    (ConnectionTestCase(name1='TestPublisher', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Remote(ip='*'), wait1=0.3,
                        name2='TestSubscriber', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Remote(), wait2=0.4,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPublisher', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(), wait1=0.3,
                        name2='TestSubscriber', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(), wait2=0.4,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPublisher', type1=Connection.SERVER, pattern1=Connection.PUB, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                        name2='TestSubscriber', type2=Connection.CLIENT, pattern2=Connection.SUB, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                        data=DATA, )),
    # Pusher / Puller - Server/Client
    (ConnectionTestCase(name1='TestPusher', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Remote(ip='*'), wait1=0.3,
                        name2='TestPuller', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Remote(), wait2=0.4,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPusher', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(), wait1=0.3,
                        name2='TestPuller', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(), wait2=0.4,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPusher', type1=Connection.SERVER, pattern1=Connection.PUSH, url1=Url.Local(local_type=Url.IPC), wait1=0.3,
                        name2='TestPuller', type2=Connection.CLIENT, pattern2=Connection.PULL, url2=Url.Local(local_type=Url.IPC), wait2=0.4,
                        data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/ Client
@pytest.mark.parametrize('test_case', TestCaseConnectionsServerClient)
def test_connections_pub_sub_pull_push_server_client(test_case):
    workers = [ConnectionSenderWorker(test_case), ConnectionReceiverWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert bytes(workers[1].result).decode('utf-8') == test_case.data


TestCaseConnectionsClientServer = [
    # Publisher / Subscribers - Client/Server
    (ConnectionTestCase(name1='TestPublisher', type1=Connection.CLIENT, pattern1=Connection.PUB, url1=Url.Remote(), wait1=0.4,
                        name2='TestSubscriber', type2=Connection.SERVER, pattern2=Connection.SUB, url2=Url.Remote(ip='*'), wait2=0.2,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPublisher', type1=Connection.CLIENT, pattern1=Connection.PUB, url1=Url.Local(), wait1=0.4,
                        name2='TestSubscriber', type2=Connection.SERVER, pattern2=Connection.SUB, url2=Url.Local(), wait2=0.2,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPublisher', type1=Connection.CLIENT, pattern1=Connection.PUB, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                        name2='TestSubscriber', type2=Connection.SERVER, pattern2=Connection.SUB, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                        data=DATA, )),
    # Pusher / Puller - Client/Server
    (ConnectionTestCase(name1='TestPusher', type1=Connection.CLIENT, pattern1=Connection.PUSH, url1=Url.Remote(), wait1=0.4,
                        name2='TestPuller', type2=Connection.SERVER, pattern2=Connection.PULL, url2=Url.Remote(ip='*'), wait2=0.2,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPusher', type1=Connection.CLIENT, pattern1=Connection.PUSH, url1=Url.Local(), wait1=0.4,
                        name2='TestPuller', type2=Connection.SERVER, pattern2=Connection.PULL, url2=Url.Local(), wait2=0.2,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestPusher', type1=Connection.CLIENT, pattern1=Connection.PUSH, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                        name2='TestPuller', type2=Connection.SERVER, pattern2=Connection.PULL, url2=Url.Local(local_type=Url.IPC), wait2=0.2,
                        data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Client / Server
@pytest.mark.parametrize('test_case', TestCaseConnectionsClientServer)
def test_connections_pub_sub_pull_push_client_server(test_case):
    workers = [ConnectionReceiverWorker(test_case), ConnectionSenderWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[1].result
    assert bytes(workers[0].result).decode('utf-8') == test_case.data


# Test Requester/Replier

# Actions for connection bind
# publisher, pusher
class ConnectionReplierWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ConnectionTestCase = test_case
        self.result = None

    def run(self) -> None:
        c = Connection(self.test_case.name1, self.test_case.type1, self.test_case.pattern1)
        c.url = self.test_case.url1
        c.open()
        req = c.recv()
        sleep(self.test_case.wait1)
        rep = c.send(str(self.test_case.data).encode("utf-8"))
        sleep(self.test_case.wait1)
        c.close()
        self.result = {
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
        c = Connection(self.test_case.name2, self.test_case.type2, self.test_case.pattern2)
        c.url = self.test_case.url2
        c.open()
        sleep(self.test_case.wait2)
        req_res = c.send(str(self.test_case.data).encode("utf-8"))
        rep = c.recv()
        sleep(self.test_case.wait2)
        c.close()
        self.result = {
            'req_result': req_res,
            'rep': rep
        }


TestCaseConnectionsRepReq = [
    # Server/Client
    (ConnectionTestCase(name1='TestReplier', pattern1=Connection.REP, type1=Connection.SERVER, url1=Url.Remote(), wait1=0.4,
                        name2='TestRequester', pattern2=Connection.REQ, type2=Connection.CLIENT, url2=Url.Remote(), wait2=0.3,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestReplier', pattern1=Connection.REP, type1=Connection.SERVER, url1=Url.Local(), wait1=0.4,
                        name2='TestRequester', pattern2=Connection.REQ, type2=Connection.CLIENT, url2=Url.Local(), wait2=0.3,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestReplier', pattern1=Connection.REP, type1=Connection.SERVER, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                        name2='TestRequester', pattern2=Connection.REQ, type2=Connection.CLIENT, url2=Url.Local(local_type=Url.IPC),
                        wait2=0.3,
                        data=DATA, )),
    # Client/Server
    (ConnectionTestCase(name1='TestReplier', pattern1=Connection.REP, type1=Connection.CLIENT, url1=Url.Remote(), wait1=0.4,
                        name2='TestRequester', pattern2=Connection.REQ, type2=Connection.SERVER, url2=Url.Remote(), wait2=0.3,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestReplier', pattern1=Connection.REP, type1=Connection.CLIENT, url1=Url.Local(), wait1=0.4,
                        name2='TestRequester', pattern2=Connection.REQ, type2=Connection.SERVER, url2=Url.Local(), wait2=0.3,
                        data=DATA, )),
    (ConnectionTestCase(name1='TestReplier', pattern1=Connection.REP, type1=Connection.CLIENT, url1=Url.Local(local_type=Url.IPC), wait1=0.4,
                        name2='TestRequester', pattern2=Connection.REQ, type2=Connection.SERVER, url2=Url.Local(local_type=Url.IPC),
                        wait2=0.3,
                        data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case', TestCaseConnectionsRepReq)
def test_connections_req_rep(test_case):
    workers = [ConnectionReplierWorker(test_case), ConnectionRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['rep_result']
    assert bytes(workers[0].result['req']).decode("utf-8") == test_case.data

    assert workers[1].result['req_result']
    assert bytes(workers[1].result['rep']).decode("utf-8") == test_case.data
