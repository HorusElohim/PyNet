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
# publisher, pusher
def thread_connection_bind(test_case: ConnectionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    usleep(200)
    res = c.send(str(test_case.data).encode("utf-8"))
    c.close()
    return res


#
# # Actions for connection connect
# # subscriber, puller
def thread_connection_connect(test_case: ConnectionTestCase):
    c = Connection(test_case.c2_name, test_case.c2_type, test_case.channel)
    c.open()
    obj = c.recv()
    c.close()
    return obj


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                 c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                 channel=Channel.Remote(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                 c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                 channel=Channel.Local(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                 c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                 channel=Channel.Local(local_type=Channel.LocalType().ipc),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                 c2_name='TestPuller', c2_type=CoreType.puller,
                                                 channel=Channel.Remote(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                 c2_name='TestPuller', c2_type=CoreType.puller,
                                                 channel=Channel.Local(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                 c2_name='TestPuller', c2_type=CoreType.puller,
                                                 channel=Channel.Local(local_type=Channel.LocalType().ipc),
                                                 data=DATA, )),
                         ])
def test_connections_pub_sub_pull_push(test_case):
    # Parallel Task
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_bind = executor.submit(thread_connection_bind, test_case)
        future_connect = executor.submit(thread_connection_connect, test_case)
        res_bind = future_bind.result()
        res_connect = future_connect.result()

        assert res_bind
        assert bytes(res_connect).decode("utf-8") == test_case.data


# Test Requester/Replier

# Actions for connection bind
# publisher, pusher
def thread_connection_replier(test_case: ConnectionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    req = c.recv()
    usleep(200)
    rep = c.send(str(test_case.data).encode("utf-8"))
    c.close()
    return {
        'req': req,
        'rep_result': rep
    }


#
# # Actions for connection connect
# # subscriber, puller
def thread_connection_requester(test_case: ConnectionTestCase):
    c = Connection(test_case.c2_name, test_case.c2_type, test_case.channel)
    c.open()
    usleep(200)
    req_res = c.send(str(test_case.data).encode("utf-8"))
    rep = c.recv()
    c.close()
    return {
        'req_result': req_res,
        'rep': rep
    }


# Test Publisher/Subscriber
# Test Pusher/Puller
@pytest.mark.parametrize('test_case',
                         [
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.replier,
                                                 c2_name='TestSubscriber', c2_type=CoreType.requester,
                                                 channel=Channel.Remote(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.replier,
                                                 c2_name='TestSubscriber', c2_type=CoreType.requester,
                                                 channel=Channel.Local(),
                                                 data=DATA, )),
                             (ConnectionTestCase(c1_name='TestPublisher', c1_type=CoreType.replier,
                                                 c2_name='TestSubscriber', c2_type=CoreType.requester,
                                                 channel=Channel.Local(local_type=Channel.LocalType().inproc),
                                                 data=DATA, )),
                         ])
def test_connections_req_rep(test_case):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_rep = executor.submit(thread_connection_replier, test_case)
        future_req = executor.submit(thread_connection_requester, test_case)
        res_rep = future_rep.result()
        res_req = future_req.result()

        assert res_rep
        assert res_req
        assert bytes(res_rep['req']).decode("utf-8") == test_case.data
        assert res_rep['rep_result']
        assert res_req['req_result']
        assert bytes(res_req['rep']).decode("utf-8") == test_case.data

