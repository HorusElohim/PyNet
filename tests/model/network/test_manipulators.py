from pynet.model.network.connection.manipulators import Serializer, Deserializer, Compressor, Decompressor
from pynet.model.network import LocalChannel, Packet
import concurrent.futures
from dataclassy import dataclass
import pytest
import copy

DATA = [1, 2, 3, 4, 6, 8, 9]
PACKET = Packet('sender', 'channel', DATA)


# _______ ConnectionDataHandle Section _______

@pytest.mark.parametrize(
    'target',
    [DATA,
     PACKET]
)
def test_serialization_handle(target):
    ser = Serializer().encode(target)
    des = Deserializer().decode(ser)
    assert target == des

