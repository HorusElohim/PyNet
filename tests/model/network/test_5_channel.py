from pynet.model.network.channels.base import BaseChannel
from pynet.model.network.core import CoreType
from pynet.model.network.url import Url, BaseUrl, RemoteUrl
from dataclassy import dataclass
from .thread_runner import WorkerRunner, Worker
import concurrent.futures
import pytest
import time


def usleep(microsecond):
    time.sleep(microsecond / 1000000.0)


DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


@dataclass(unsafe_hash=True, slots=True)
class ChannelTestCase:
    c1_name: str
    c2_name: str
    c1_type: CoreType
    c2_type: CoreType
    url: BaseUrl
    compression: bool
    data: object


# WORKER
class ChannelWorker(Worker):
    def __init__(self, test_case):
        Worker.__init__(self)
        self.test_case: ChannelTestCase = test_case
        self.result = None


# Actions for connection bind
# publisher, pusher
class ChannelBindWorker(ChannelWorker):
    def run(self) -> None:
        if isinstance(self.test_case.url, RemoteUrl):
            self.test_case.url.ip = '*'
        c = BaseChannel(self.test_case.c1_name, self.test_case.c1_type)
        c.add(f'Test-{self.test_case.c1_type}', self.test_case.url)
        usleep(12000)
        res = c._send(self.test_case.data, compression=self.test_case.compression)
        c.close()
        self.result = res[0]


# # Actions for connection connect
# # subscriber, puller
class ChannelConnectWorker(ChannelWorker):
    def run(self) -> None:
        c = BaseChannel(self.test_case.c2_name, self.test_case.c2_type)
        c.add(f'Test-{self.test_case.c2_type}', self.test_case.url)
        data = c._recv()
        c.close()
        self.result = data[0]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             # Without Compression
                             (ChannelTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                              c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                              url=Url.Remote(), compression=False, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                              c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                              url=Url.Local(), compression=False, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                              c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                              url=Url.Local(local_type=Url.LocalType().ipc),
                                              compression=False, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                              c2_name='TestPuller', c2_type=CoreType.puller,
                                              url=Url.Remote(), compression=False, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                              c2_name='TestPuller', c2_type=CoreType.puller,
                                              url=Url.Local(), compression=False, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                              c2_name='TestPuller', c2_type=CoreType.puller,
                                              url=Url.Local(local_type=Url.LocalType().ipc),
                                              compression=False, data=DATA, )),
                             # With Compression
                             (ChannelTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                              c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                              url=Url.Remote(), compression=True, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                              c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                              url=Url.Local(), compression=True, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                              c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                              url=Url.Local(local_type=Url.LocalType().ipc),
                                              compression=True, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                              c2_name='TestPuller', c2_type=CoreType.puller,
                                              url=Url.Remote(), compression=True, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                              c2_name='TestPuller', c2_type=CoreType.puller,
                                              url=Url.Local(), compression=True, data=DATA, )),
                             (ChannelTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                              c2_name='TestPuller', c2_type=CoreType.puller,
                                              url=Url.Local(local_type=Url.LocalType().ipc),
                                              compression=True, data=DATA, )),
                         ])
def test_channel_pub_sub_push_pull(test_case):
    workers = [ChannelBindWorker(test_case), ChannelConnectWorker(test_case)]
    WorkerRunner.run(workers)

    assert workers[0].result
    assert workers[1].result == test_case.data


# Actions for connection bind
# replier
class ChannelReplierWorker(ChannelWorker):
    def run(self) -> None:
        c = BaseChannel(self.test_case.c1_name, self.test_case.c1_type)
        c.add(f'Test-{self.test_case.c1_name}', self.test_case.url)
        req = c._recv()
        usleep(5000)
        rep = c._send(self.test_case.data, self.test_case.compression)
        c.close()
        self.result = {
            'req': req[0],
            'rep_result': rep
        }


# Actions for connection connect
# requester
class ChannelRequesterWorker(ChannelWorker):
    def run(self) -> None:
        c = BaseChannel(self.test_case.c2_name, self.test_case.c2_type)
        c.add(f'Test-{self.test_case.c2_name}', self.test_case.url)
        usleep(8000)
        req_res = c._send(self.test_case.data, self.test_case.compression)
        usleep(8000)
        rep = c._recv()
        c.close()
        self.result = {
            'req_result': req_res,
            'rep': rep[0]
        }


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (ChannelTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                              c2_name='TestRequester', c2_type=CoreType.requester,
                                              url=Url.Remote(),
                                              data=DATA, compression=False)),
                             (ChannelTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                              c2_name='TestRequester', c2_type=CoreType.requester,
                                              url=Url.Local(),
                                              data=DATA, compression=False)),
                             (ChannelTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                              c2_name='TestRequester', c2_type=CoreType.requester,
                                              url=Url.Local(local_type=Url.LocalType().inproc),
                                              data=DATA, compression=False)),
                             (ChannelTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                              c2_name='TestRequester', c2_type=CoreType.requester,
                                              url=Url.Remote(),
                                              data=DATA, compression=True)),
                             (ChannelTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                              c2_name='TestRequester', c2_type=CoreType.requester,
                                              url=Url.Local(),
                                              data=DATA, compression=True)),
                             (ChannelTestCase(c1_name='TestReplier', c1_type=CoreType.replier,
                                              c2_name='TestRequester', c2_type=CoreType.requester,
                                              url=Url.Local(local_type=Url.LocalType().inproc),
                                              data=DATA, compression=True)),
                         ])
def test_connections_req_rep(test_case):
    workers = [ChannelReplierWorker(test_case), ChannelRequesterWorker(test_case)]
    WorkerRunner.run(workers)

    assert workers[0].result
    assert workers[1].result
    assert workers[0].result['req'] == test_case.data
    assert workers[0].result['rep_result']
    assert workers[1].result['req_result']
    assert workers[1].result['rep'] == test_case.data
