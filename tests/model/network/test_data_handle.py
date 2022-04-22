from pynet.model.network import DataHandle, Packet
import copy

DATA = [1, 2, 3, 4, 6, 8, 9]
PACKET = Packet('sender', 'channel', DATA)


def test_data_handle_obj():
    enc = DataHandle.encode(DATA)
    dec = DataHandle.decode(enc)
    assert dec == DATA


def test_data_handle_packet_default():
    pkt = copy.deepcopy(PACKET)
    enc = DataHandle.encode(pkt)
    dec = DataHandle.decode(enc)
    assert dec == PACKET


def test_data_handle_packet_no_enc():
    pkt = copy.deepcopy(PACKET)
    enc = DataHandle.encode(pkt, data_encode=True)
    dec = DataHandle.decode(enc)
    assert dec == PACKET


def test_data_handle_packet_enc_no_comp():
    pkt = copy.deepcopy(PACKET)
    enc = DataHandle.encode(pkt, data_compress=False)
    dec = DataHandle.decode(enc)
    assert dec == PACKET


def test_data_handle_packet_no_enc_comp():
    pkt = copy.deepcopy(PACKET)
    enc = DataHandle.encode(pkt, data_encode=False, data_compress=True)
    dec = DataHandle.decode(enc)
    assert dec == PACKET


def test_data_handle_packet_no_enc_no_comp():
    pkt = copy.deepcopy(PACKET)
    enc = DataHandle.encode(pkt, data_encode=False, data_compress=False)
    dec = DataHandle.decode(enc)
    assert dec == PACKET
