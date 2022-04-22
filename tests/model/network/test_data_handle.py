from pynet.model.network import DataHandle, Packet

DATA = [1, 2, 3, 4, 6, 8, 9]


def test_data_handle_obj():
    enc = DataHandle.encode(DATA)
    dec = DataHandle.decode(enc)
    assert dec == DATA
