from pynet.model.network import Connection, LocalChannel, RemoteChannel, LocalChannelType, Packet
import copy
import pytest

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
    if isinstance(target, Packet):
        input_target = copy.deepcopy(target)
        enc = Connection.encode(Connection.encode_packet(input_target), compression=compression)
        dec = Connection.decode_packet(Connection.decode(enc))
        assert dec == target
    else:
        enc = Connection.encode(target, compression=compression)
        dec = Connection.decode(enc)
        assert dec == target

# ___________________________________________
