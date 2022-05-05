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
    usleep(200)
    res = c.send(test_case.data, compression=test_case.compression)
    c.close()
    return res[0]


#
# # Actions for connection connect
# # subscriber, puller
def thread_connection_connect(test_case: ChannelTestCase):
    c = BaseChannel(test_case.c2_name, test_case.c2_type)
    c.add(f'Test-{test_case.c2_type}', test_case.url)
    data = c.recv()
    c.close()
    return data[0]


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
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
