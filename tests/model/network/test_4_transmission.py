from pynet.model.network.transmission import Packet, Transmission, Connection
from pynet.model.network.core import CoreType
from pynet.model.network.url import Url, BaseUrl
from dataclassy import dataclass
import concurrent.futures
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


# Actions for connection bind
# publisher, pusher
def thread_connection_bind(test_case: TransmissionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    usleep(5000)
    res = Transmission.send(c, test_case.data, compression=test_case.compression)
    c.close()
    return res


#
# # Actions for connection connect
# # subscriber, puller
def thread_connection_connect(test_case: TransmissionTestCase):
    c = Connection(test_case.c2_name, test_case.c2_type, test_case.channel)
    c.open()
    data = Transmission.recv(c)
    c.close()
    return data


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
