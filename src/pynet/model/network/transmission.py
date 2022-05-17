from .. import Logger, Size
from .packet import Packet
from .connection import Connection, RECV_ERROR
from typing import Any
import hashlib
import blosc2
import pickle

TRANS_LOG = Logger('Transmission')
TRANS_LOG.log.debug('Module Init')


def compress(byte: bytes) -> Any:
    return blosc2.compress(byte, cname='zlib')


def decompress(compress_byte: bytes) -> Any:
    return blosc2.decompress(compress_byte)


def hashing(bytes_obg: bytes) -> str:
    md5 = hashlib.md5(bytes_obg)
    return md5.hexdigest()


def encode(obj: object) -> bytes:
    return pickle.dumps(obj)


def decode(compress_byte: bytes) -> object:
    return pickle.loads(compress_byte)


class Transmission:
    @staticmethod
    def to_packet(con_name: str,  # type: ignore[misc]
                  data: Any,
                  seq_left: int = 0,
                  compression: bool = False) -> Packet:
        pkt = Packet(con_name, data, seq_left)
        pkt.data = encode(pkt.data)
        TRANS_LOG.log.debug('encoded')
        pkt.encoded = True
        if compression:
            pkt.data = compress(pkt.data)
            TRANS_LOG.log.debug('compressed')
            pkt.compressed = True
        TRANS_LOG.log.debug(
            f'Pkt: {pkt} size {Size.pretty_obj_size(pkt)} with data data: {Size.pretty_obj_size(pkt.data)}')
        return pkt

    @staticmethod
    def from_packet(pkt: Packet) -> Any:  # type: ignore[misc]
        TRANS_LOG.log.debug(
            f'from Pkt: {pkt} size {Size.pretty_obj_size(pkt)} with data: {Size.pretty_obj_size(pkt.data)}')
        if pkt.compressed:
            assert isinstance(pkt.data, bytes)
            pkt.compressed = False
            pkt.data = decompress(pkt.data)
            TRANS_LOG.log.debug('decompressed')
        if pkt.encoded:
            pkt.encoded = False
            pkt.data = decode(pkt.data)  # type: ignore[arg-type]
            TRANS_LOG.log.debug('decoded')
        return pkt.data

    @staticmethod
    def send(con: Connection, data: Any, seq_left: int = 0, compression: bool = False) -> bool:  # type: ignore[misc]
        res = con._send(encode(Transmission.to_packet(con._connection_name, data, seq_left, compression)))
        if res:
            TRANS_LOG.log.debug('success')
        else:
            TRANS_LOG.log.error('failed')
        return res

    @staticmethod
    def recv(con: Connection, wait=True) -> Any:  # type: ignore[misc]
        raw = con._recv(wait)
        if raw == RECV_ERROR:
            TRANS_LOG.log.error('failed')
            return RECV_ERROR
        pkt: Packet = decode(raw)  # type: ignore[arg-type]
        data = Transmission.from_packet(pkt)
        if data:
            TRANS_LOG.log.debug('success')
        else:
            TRANS_LOG.log.error('failed')
        return data


TRANS_LOG.log.debug('Module Loader')
