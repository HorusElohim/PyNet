from pynet.model.network.transmission import Packet, Transmission, Connection
from pynet.model.network.core import CoreType
from pynet.model.network.channel import Channel

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
