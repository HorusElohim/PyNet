from pynet.model.network.pattern import *
from pynet.model.network import BaseChannel, LocalChannel, RemoteChannel
import concurrent.futures
import pytest
from zmq import Context

CTX = Context()
DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Actions for connection bind
# publisher, replier, puller
def thread_create_publisher_patter(channel: BaseChannel):
    pub = Publisher('Publisher', channel, CTX)
    res = pub.send(DATA)
    return res


# Actions for connection connect
# subscriber, requester, pusher
def thread_create_subscriber_patter(channel: BaseChannel):
    sub = Subscriber('Subscriber', channel, CTX)
    data = sub.receive()
    return data


@pytest.mark.parametrize('channel',
                         [
                             (LocalChannel()),
                         ])
def test_base_patter_pub_sub_transmission(channel: BaseChannel):
    pass
    # Parallel Task
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future_pub = executor.submit(thread_create_publisher_patter, channel)
    #     future_sub = executor.submit(thread_create_subscriber_patter, channel)
    #     assert future_pub.result()
    #     assert future_sub.result() == DATA
