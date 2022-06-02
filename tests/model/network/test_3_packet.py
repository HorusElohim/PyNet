from pynet.model.network.packet import Packet


def test_packet():
    p = Packet('sender', None)
    assert p.sender == 'sender'
    assert p.data is None
    assert p.size == '224 byte'
