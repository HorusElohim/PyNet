from pynet.model.network.channels.base import BaseChannel
from pynet.model.network.core import CoreType
from pynet.model.network.url import Url, BaseUrl
from dataclassy import dataclass
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


# Actions for connection bind
# publisher, pusher
def thread_connection_bind(test_case: ChannelTestCase):
    c = BaseChannel(test_case.c1_name, test_case.c1_type)
    c.add(f'Test-{test_case.c1_type}', test_case.url)
    usleep(8000)
    res = c._send(test_case.data, compression=test_case.compression)
    usleep(8000)
    c.close()
    return res[0]


#
# # Actions for connection connect
# # subscriber, puller
def thread_connection_connect(test_case: ChannelTestCase):
    c = BaseChannel(test_case.c2_name, test_case.c2_type)
    c.add(f'Test-{test_case.c2_type}', test_case.url)
    data = c._recv()
    c.close()
    return data[0]


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
    # Parallel Task
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_bind = executor.submit(thread_connection_bind, test_case)
        future_connect = executor.submit(thread_connection_connect, test_case)
        res_bind = future_bind.result()
        res_connect = future_connect.result()

        assert res_bind
        assert res_connect == test_case.data


# Actions for connection bind
# replier
def thread_connection_replier(test_case: ChannelTestCase):
    c = BaseChannel(test_case.c1_name, test_case.c1_type)
    c.add(f'Test-{test_case.c1_name}', test_case.url)
    req = c._recv()
    usleep(5000)
    rep = c._send(test_case.data, test_case.compression)
    c.close()
    return {
        'req': req[0],
        'rep_result': rep
    }


#
# Actions for connection connect
# requester
def thread_connection_requester(test_case: ChannelTestCase):
    c = BaseChannel(test_case.c2_name, test_case.c2_type)
    c.add(f'Test-{test_case.c2_name}', test_case.url)
    usleep(8000)
    req_res = c._send(test_case.data, test_case.compression)
    usleep(8000)
    rep = c._recv()
    c.close()
    return {
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
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_rep = executor.submit(thread_connection_replier, test_case)
        future_req = executor.submit(thread_connection_requester, test_case)
        res_rep = future_rep.result()
        res_req = future_req.result()

        assert res_rep
        assert res_req
        assert res_rep['req'] == test_case.data
        assert res_rep['rep_result']
        assert res_req['req_result']
        assert res_req['rep'] == test_case.data
