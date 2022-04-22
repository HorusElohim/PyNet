from pynet.model.network import Packet


def test_packet():
    p = Packet('sender', 'channel', None)
    assert p.sender == 'sender'
    assert p.channel == 'channel'
    assert p.data is None
    assert p.size == '304 byte'
