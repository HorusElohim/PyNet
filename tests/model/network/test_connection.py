from pynet.model.network import Connection, LocalChannel, RemoteChannel, LocalChannelType, Packet, BaseChannel
import concurrent.futures
from dataclassy import dataclass
import pytest
import copy

DATA = [1, 2, 3, 4, 6, 8, 9]
PACKET = Packet('sender', 'channel', DATA)
CHANNEL = LocalChannel()


# _______ ConnectionBase Section _______

@pytest.mark.parametrize(
    'connection_type, channel_type',
    [
        (Connection.Type.publisher, LocalChannel(local_type=LocalChannelType.inproc)),
        (Connection.Type.subscriber, LocalChannel(local_type=LocalChannelType.inproc)),
        (Connection.Type.puller, LocalChannel(local_type=LocalChannelType.inproc)),
        (Connection.Type.pusher, LocalChannel(local_type=LocalChannelType.inproc)),
        (Connection.Type.replier, LocalChannel(local_type=LocalChannelType.inproc)),
        (Connection.Type.requester, LocalChannel(local_type=LocalChannelType.inproc)),

        (Connection.Type.publisher, LocalChannel(local_type=LocalChannelType.ipc)),
        (Connection.Type.subscriber, LocalChannel(local_type=LocalChannelType.ipc)),
        (Connection.Type.puller, LocalChannel(local_type=LocalChannelType.ipc)),
        (Connection.Type.pusher, LocalChannel(local_type=LocalChannelType.ipc)),
        (Connection.Type.replier, LocalChannel(local_type=LocalChannelType.ipc)),
        (Connection.Type.requester, LocalChannel(local_type=LocalChannelType.ipc)),

        (Connection.Type.publisher, RemoteChannel()),
        (Connection.Type.subscriber, RemoteChannel()),
        (Connection.Type.puller, RemoteChannel()),
        (Connection.Type.pusher, RemoteChannel()),
        (Connection.Type.replier, RemoteChannel()),
        (Connection.Type.requester, RemoteChannel()),

    ])
def test_connection_base(connection_type, channel_type):
    c = Connection('test', connection_type, channel_type)
    assert c is not None
    assert c.channel == channel_type
    assert c.open
    assert c.type == connection_type
    c.close()


# ___________________________________________

# _______ ConnectionDataHandle Section _______

@pytest.mark.parametrize(
    'target, compression',
    [
        (DATA, True),
        (DATA, False),
        (PACKET, False),
    ]
)
def test_connection_data_handle(target, compression):
    c = Connection('Test', Connection.Type.publisher, LocalChannel())
    if isinstance(target, Packet):
        input_target = copy.deepcopy(target)
        enc = c.encode(c.encode_packet(input_target), compression=compression)
        dec = c.decode_packet(c.decode(enc))
        assert dec == target
    else:
        enc = c.encode(target, compression=compression)
        dec = c.decode(enc)
        assert dec == target
    c.close()


# ___________________________________________

# _______ ConnectionTransmission Section _______

@dataclass(unsafe_hash=True, slots=True)
class TransmissionTestCase:
    c1_name: str
    c2_name: str
    c1_type: Connection.Type
    c2_type: Connection.Type
    channel: BaseChannel
    data: object
    raw: bool


# Actions for connection bind
# publisher, replier, puller
def thread_connection_bind(test_case: TransmissionTestCase):
    c = Connection(test_case.c1_name, test_case.c1_type, test_case.channel)
    res = c.send(test_case.data)
    c.close()
    return res


# Actions for connection connect
# subscriber, requester, pusher
def thread_connection_connect(test_case: TransmissionTestCase):
    c = Connection(test_case.c2_name, test_case.c2_type, test_case.channel)
    obj = c.receive(test_case.raw)
    c.close()
    return obj


@pytest.mark.parametrize('test_case',
                         [
                             (TransmissionTestCase(c1_name='sender', c1_type=Connection.Type.publisher,
                                                   c2_name='receiver', c2_type=Connection.Type.subscriber,
                                                   channel=LocalChannel(),
                                                   data=DATA,
                                                   raw=True)),
                             (TransmissionTestCase(c1_name='sender', c1_type=Connection.Type.pusher,
                                                   c2_name='receiver', c2_type=Connection.Type.puller,
                                                   channel=LocalChannel(),
                                                   data=DATA,
                                                   raw=True)),
                         ])
def test_connection_transmission(test_case):
    # Parallel Task
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_connect = executor.submit(thread_connection_connect, test_case)
        future_bind = executor.submit(thread_connection_bind, test_case)
        res_connect = future_connect.result()
        res_bind = future_bind.result()

    assert res_bind
    if test_case.raw:
        assert isinstance(res_connect, Packet)
        assert res_connect.data == test_case.data
    else:
        assert isinstance(res_connect, list)
        assert res_connect == test_case.data

# ___________________________________________
