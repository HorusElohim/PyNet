from pynet.model.network import Packet


def test_packet():
    p = Packet('sender', 'channel', None)
    assert p.info.sender == 'sender'
    assert p.info.channel == 'channel'
    assert p.data is None
    assert p.size == '344 byte'
