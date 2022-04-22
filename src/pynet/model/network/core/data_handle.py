from . import Packet, Manipulator
from typing import Union, ByteString


class DataHandle:
    """
        Packet Handle
        Used to encode and decode the Packet
    """

    @staticmethod
    def _decode_(serialized_data: Union[bytes, ByteString]) -> object:
        return Manipulator.decode(serialized_data)

    @staticmethod
    def _encode_(obj: object, compression: bool = False) -> bytes:
        enc = Manipulator.encode(obj)
        if compression:
            enc = Manipulator.compress(enc)
        return enc

    @staticmethod
    def _decode_packet(packet: Packet) -> Packet:
        if packet.info.compressed:
            # Decompress
            packet.data = Manipulator.decompress(packet.data)
            packet.info.compressed = False
        if packet.info.encoded:
            # Decode
            packet.data = Manipulator.decode(packet.data)
            packet.info.encoded = False
        return packet

    @staticmethod
    def _encode_packet(packet: Packet, data_encode: bool = True, data_compress: bool = True) -> Packet:
        if data_encode and not packet.info.encoded:
            # Encode Data
            packet.data = Manipulator.encode(packet.data)
            packet.info.encoded = True
        if data_compress and not packet.info.compressed:
            # Compress Data
            packet.data = Manipulator.compress(packet.data)
            packet.info.compressed = True
        return packet

    @staticmethod
    def decode(serialized_data: Union[bytes, ByteString]) -> Union[Packet, object]:
        """
        Decode Function

        :param: serialized_data:
        :return: Decoded Packet or Object

        """
        obj = DataHandle._decode_(serialized_data)
        if isinstance(obj, Packet):
            obj = DataHandle._decode_packet(obj)

        return obj

    @staticmethod
    def encode(target: Union[Packet, object], data_encode: bool = True, data_compress: bool = True) -> bytes:
        """
        Encode Function

        :param: target: a Packet or Python Object
        :param: data_encode: Flag to encode the Packet Data
        :param: data_compress: Flag to compress the Packet Data

        :return: Encoded Packet or Object

        """

        if isinstance(target, Packet):
            target = DataHandle._encode_packet(target, data_encode, data_compress)

        return DataHandle._encode_(target)
