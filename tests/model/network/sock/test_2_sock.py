from pynet.model.network.sock import Sock
from pynet.model import Logger
from dataclassy import dataclass
from ..thread_runner import Worker, WorkerRunner
import pytest
from time import sleep

DATA = "TestData"

TEST_LOG = Logger('test_2_sock')


@dataclass(unsafe_hash=True, slots=True)
class SockTestCase:
    name1: str
    name2: str
    pattern1: Sock.Pattern
    pattern2: Sock.Pattern
    wait1: float
    wait2: float
    url1: Sock.SockUrl.Abc
    url2: Sock.SockUrl.Abc
    data: object


# Actions for connection bind
# publisher, pusher
class SockSenderWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: SockTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name1, self.test_case.pattern1, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url1
        sock.open()
        sleep(self.test_case.wait1)
        self.result = sock._send(str(self.test_case.data).encode("utf-8"))
        sleep(self.test_case.wait1)
        sock.close()


# # Actions for connection connect
# # subscriber, puller
class SockReceiverWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: SockTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name2, self.test_case.pattern2, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url2
        sock.open()
        sleep(self.test_case.wait2)
        self.result = sock._recv()
        sock.close()


TestCaseSocksServerClient = [
    # Publisher / Subscribers - Server/Client
    (SockTestCase(name1='TestPublisher', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                  name2='TestSubscriber', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                  data=DATA, )),
    (SockTestCase(name1='TestPublisher', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.3,
                  name2='TestSubscriber', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                  data=DATA, )),
    (SockTestCase(name1='TestPublisher', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), wait1=0.3,
                  name2='TestSubscriber', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                  wait2=0.4,
                  data=DATA, )),
    # Pusher / Puller - Server/Client
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                  name2='TestPuller', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, ), wait1=0.3,
                  name2='TestPuller', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), wait1=0.3,
                  name2='TestPuller', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), wait2=0.4,
                  data=DATA, )),
    # Pair - Server/Client
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait1=0.3,
                  name2='TestPuller', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.4,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, ), wait1=0.3,
                  name2='TestPuller', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.4,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), wait1=0.3,
                  name2='TestPuller', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), wait2=0.4,
                  data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Server/ Client
@pytest.mark.parametrize('test_case', TestCaseSocksServerClient)
def test_connections_pub_sub_pull_push_server_client(test_case):
    workers = [SockSenderWorker(test_case), SockReceiverWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert bytes(workers[1].result).decode('utf-8') == test_case.data


TestCaseSocksClientServer = [
    # Publisher / Subscribers - Client/Server
    (SockTestCase(name1='TestPublisher', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestSubscriber', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.2,
                  data=DATA, )),
    (SockTestCase(name1='TestPublisher', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestSubscriber', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, ), wait2=0.2,
                  data=DATA, )),
    (SockTestCase(name1='TestPublisher', pattern1=Sock.Pattern.publisher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), wait1=0.4,
                  name2='TestSubscriber', pattern2=Sock.Pattern.subscriber, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                  wait2=0.2,
                  data=DATA, )),
    # Pusher / Puller - Client/Server
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestPuller', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.2,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestPuller', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.2, data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pusher, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), wait1=0.4,
                  name2='TestPuller', pattern2=Sock.Pattern.puller, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), wait2=0.2,
                  data=DATA, )),
    # Pair - Client/Server
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestPuller', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER, ip='*'), wait2=0.2,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestPuller', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.2,
                  data=DATA, )),
    (SockTestCase(name1='TestPusher', pattern1=Sock.Pattern.pair, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), wait1=0.4,
                  name2='TestPuller', pattern2=Sock.Pattern.pair, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), wait2=0.2,
                  data=DATA, )),

]


# Test Publisher/Subscriber
# Test Pusher/Puller
# Client / Server
@pytest.mark.parametrize('test_case', TestCaseSocksClientServer)
def test_connections_pub_sub_pull_push_client_server(test_case):
    workers = [SockReceiverWorker(test_case), SockSenderWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[1].result
    assert bytes(workers[0].result).decode('utf-8') == test_case.data


# Test Requester/Replier

# Actions for connection bind
# publisher, pusher
class SockReplierWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: SockTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name1, self.test_case.pattern1, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url1
        sock.open()
        req = sock._recv()
        sleep(self.test_case.wait1)
        rep = sock._send(str(self.test_case.data).encode("utf-8"))
        sleep(self.test_case.wait1)
        sock.close()
        self.result = {
            'req': req,
            'rep_result': rep
        }


#
# # Actions for connection connect
# # subscriber, puller
class SockRequesterWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: SockTestCase = test_case
        self.result = None

    def run(self) -> None:
        sock = Sock(self.test_case.name2, self.test_case.pattern2, logger_other=TEST_LOG)
        sock.sock_urls = self.test_case.url2
        sock.open()
        sleep(self.test_case.wait2)
        req_res = sock._send(str(self.test_case.data).encode("utf-8"))
        rep = sock._recv()
        sleep(self.test_case.wait2)
        sock.close()
        self.result = {
            'req_result': req_res,
            'rep': rep
        }


TestCaseSocksRepReq = [
    # Server/Client
    (SockTestCase(name1='TestReplier', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Remote(Sock.SockUrl.SERVER), wait1=0.4,
                  name2='TestRequester', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait2=0.3,
                  data=DATA, )),
    (SockTestCase(name1='TestReplier', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait1=0.4,
                  name2='TestRequester', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait2=0.3,
                  data=DATA, )),
    (SockTestCase(name1='TestReplier', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), wait1=0.4,
                  name2='TestRequester', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC),
                  wait2=0.3,
                  data=DATA, )),
    # Client/Server
    (SockTestCase(name1='TestReplier', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestRequester', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Remote(Sock.SockUrl.SERVER), wait2=0.3,
                  data=DATA, )),
    (SockTestCase(name1='TestReplier', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT), wait1=0.4,
                  name2='TestRequester', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER), wait2=0.3,
                  data=DATA, )),
    (SockTestCase(name1='TestReplier', pattern1=Sock.Pattern.replier, url1=Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), wait1=0.4,
                  name2='TestRequester', pattern2=Sock.Pattern.requester, url2=Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC),
                  wait2=0.3,
                  data=DATA, )),
]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case', TestCaseSocksRepReq)
def test_connections_req_rep(test_case):
    workers = [SockReplierWorker(test_case), SockRequesterWorker(test_case)]
    WorkerRunner.run(workers)
    assert workers[0].result
    assert workers[1].result

    assert workers[0].result['rep_result']
    assert bytes(workers[0].result['req']).decode("utf-8") == test_case.data

    assert workers[1].result['req_result']
    assert bytes(workers[1].result['rep']).decode("utf-8") == test_case.data
