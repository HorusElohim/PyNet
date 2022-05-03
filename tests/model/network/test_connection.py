from pynet.model.network.connection import Connection, CoreType
from dataclassy import dataclass
from pynet.model.network.channel import Channel, BaseChannel
import concurrent.futures
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
        (CoreType.publisher, Channel.Local(local_type=Channel.LocalType().ipc)),
        (CoreType.subscriber, Channel.Local(local_type=Channel.LocalType().ipc)),
        (CoreType.puller, Channel.Local(local_type=Channel.LocalType().ipc)),
        (CoreType.pusher, Channel.Local(local_type=Channel.LocalType().ipc)),
        (CoreType.replier, Channel.Local(local_type=Channel.LocalType().ipc)),
        (CoreType.requester, Channel.Local(local_type=Channel.LocalType().ipc)),

        (CoreType.publisher, Channel.Local(local_type=Channel.LocalType().inproc)),
        (CoreType.subscriber, Channel.Local(local_type=Channel.LocalType().inproc)),
        (CoreType.puller, Channel.Local(local_type=Channel.LocalType().inproc)),
        (CoreType.pusher, Channel.Local(local_type=Channel.LocalType().inproc)),
        (CoreType.replier, Channel.Local(local_type=Channel.LocalType().inproc)),
        (CoreType.requester, Channel.Local(local_type=Channel.LocalType().inproc)),

        (CoreType.publisher, Channel.Remote(port=28128)),
        (CoreType.subscriber, Channel.Remote(port=28128)),
        (CoreType.puller, Channel.Remote(port=28129)),
        (CoreType.pusher, Channel.Remote(port=28129)),
        (CoreType.replier, Channel.Remote(port=28130)),
        (CoreType.requester, Channel.Remote(port=28130)),

    ])
def test_connection_creation(connection_type, channel_type):
    c = Connection('TestConnectionCreation', connection_type, channel_type)
    assert c is not None
    c.open()
    assert c.is_open()
    assert c.channel == channel_type
    assert c.core_type == connection_type
    c.close()
    assert not c.is_open()


@dataclass(unsafe_hash=True, slots=True)
class ConnectionTestCase:
    c1_name: str
    c2_name: str
    c1_type: CoreType
    c2_type: CoreType
    channel: BaseChannel
    data: object


# Actions for connection bind
# publisher, replier, puller
def thread_connection_bind(test_case: ConnectionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    res = c.send(test_case.data)
    c.close()
    return res


#
# # Actions for connection connect
# # subscriber, requester, pusher
def thread_connection_connect(test_case: ConnectionTestCase):
    c = Connection(test_case.c2_name, test_case.c2_type, test_case.channel)
    c.open()
    obj = c.recv()
    c.close()
    return obj


#

@pytest.mark.parametrize('test_case',
                         [
                             (ConnectionTestCase(c1_name='sender', c1_type=CoreType.publisher,
                                                 c2_name='receiver', c2_type=CoreType.subscriber,
                                                 channel=Channel.Local(local_type=Channel.LocalType().ipc),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='sender', c1_type=CoreType.pusher,
                                                 c2_name='receiver', c2_type=CoreType.puller,
                                                 channel=Channel.Local(), data=DATA, )),
                         ])
def test_connection_transmission(test_case):
    # Parallel Task

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_bind = executor.submit(thread_connection_bind, test_case)
        usleep(100)
        future_connect = executor.submit(thread_connection_connect, test_case)
        res_bind = future_bind.result()
        res_connect = future_connect.result()

    assert res_bind
    assert isinstance(res_connect, list)
    assert res_connect == test_case.data

# ___________________________________________
