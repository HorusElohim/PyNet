from .packet import Packet
from .sock import Sock
from typing import Any
from .. import encode, decode, compress, decompress


class Transmission:
    @staticmethod
    def to_packet(sock_name: str,  # type: ignore[misc]
                  data: Any,
                  seq_left: int = 0,
                  compression: bool = False) -> Packet:
        pkt = Packet(sock_name, data, seq_left)
        pkt.data = encode(pkt.data)
        pkt.encoded = True
        if compression:
            pkt.data = compress(pkt.data)
            pkt.compressed = True
        return pkt

    @staticmethod
    def from_packet(pkt: Packet) -> Any:  # type: ignore[misc]
        if pkt.compressed:
            assert isinstance(pkt.data, bytes)
            pkt.compressed = False
            pkt.data = decompress(pkt.data)
        if pkt.encoded:
            pkt.encoded = False
            pkt.data = decode(pkt.data)  # type: ignore[arg-type]
        return pkt.data

    @staticmethod
    def send(sock: Sock, data: Any, flag: int = 0, seq_left: int = 0, compression: bool = False) -> bool:  # type: ignore[misc]
        res = sock._send(encode(Transmission.to_packet(sock.entity_name, data, seq_left, compression)), flag)
        if res:
            sock.log.debug('success')
        else:
            sock.log.error('failed')
        return res

    @staticmethod
    def recv(sock: Sock, flag: int = 0) -> Any:  # type: ignore[misc]
        raw = sock._recv(flag)
        if raw == sock.RECV_ERROR:
            sock.log.error('failed')
            return sock.RECV_ERROR
        pkt: Packet = decode(raw)  # type: ignore[arg-type, assignment]
        data = Transmission.from_packet(pkt)
        if data is not None:
            sock.log.debug('success')
        else:
            sock.log.error('failed')
        return data
