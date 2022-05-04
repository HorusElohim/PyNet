from pynet.model.network.transmission import Packet, Transmission, Connection
from pynet.model.network.core import CoreType
from pynet.model.network.channel import Channel, BaseChannel
from dataclassy import dataclass
import concurrent.futures
import pytest
import time


def usleep(microsecond):
    time.sleep(microsecond / 1000000.0)


DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_transmission_packets():
    c = Connection('Transmission', CoreType.publisher, Channel.Local())
    pkt = Transmission.to_packet(c, DATA)
    data = Transmission.from_packet(pkt)
    assert pkt.encoded
    assert data == DATA


def test_transmission_compressed_packets():
    c = Connection('Transmission', CoreType.publisher, Channel.Local())
    pkt = Transmission.to_packet(c, DATA, compression=True)
    data = Transmission.from_packet(pkt)
    assert pkt.encoded
    assert data == DATA


@dataclass(unsafe_hash=True, slots=True)
class TransmissionTestCase:
    c1_name: str
    c2_name: str
    c1_type: CoreType
    c2_type: CoreType
    channel: BaseChannel
    compression: bool
    data: object


# Actions for connection bind
# publisher, pusher
def thread_connection_bind(test_case: TransmissionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    c.open()
    usleep(200)
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
                                                   channel=Channel.Remote(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Channel.Local(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Channel.Local(local_type=Channel.LocalType().ipc),
                                                   compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Channel.Remote(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Channel.Local(), compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Channel.Local(local_type=Channel.LocalType().ipc),
                                                   compression=False, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Channel.Remote(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Channel.Local(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPublisher', c1_type=CoreType.publisher,
                                                   c2_name='TestSubscriber', c2_type=CoreType.subscriber,
                                                   channel=Channel.Local(local_type=Channel.LocalType().ipc),
                                                   compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Channel.Remote(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Channel.Local(), compression=True, data=DATA, )),
                             (TransmissionTestCase(c1_name='TestPusher', c1_type=CoreType.pusher,
                                                   c2_name='TestPuller', c2_type=CoreType.puller,
                                                   channel=Channel.Local(local_type=Channel.LocalType().ipc),
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
