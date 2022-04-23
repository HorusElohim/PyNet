from __future__ import annotations
from zmq import (
    Context, Socket, ZMQError,
    SUB, PUB, REQ, REP, PUSH, PULL,
    SUBSCRIBE
)
from typing import Union, Any, ByteString, List
from dataclassy import dataclass
from enum import Enum
import hashlib
import blosc2
import pickle

from ...common import Logger
from . import BaseChannel, Packet


@dataclass(slots=True)
class ConnectionBase(Logger):
    """
        Connection Class
        Used to manage the zmq socket

    """

    class Type(Enum):
        """
        Type of Connection
        """
        subscriber = SUB
        publisher = PUB
        replier = REP
        requester = REQ
        pusher = PUSH
        puller = PULL
        helper = -100

    name: str
    type: Type
    socket: Socket
    channel: BaseChannel
    open: bool
    __bind_types: List[Type]
    __connect_types: List[Type]

    def __init__(self, name: str, connection_type: Type, channel: BaseChannel, context: Context = Context.instance()):
        """

        :param connection_type: Connection Type
        :param channel: Target Channel
        :param context: ZMQ Context

        """
        self.name = name
        self.type = connection_type
        self.channel = channel
        self.socket = context.socket(self.type.value)
        self.open = False
        self.__bind_types = [self.Type.publisher, self.Type.replier, self.Type.puller]
        self.__connect_types = [self.Type.subscriber, self.Type.requester, self.Type.pusher]

        try:
            if self.type in self.__bind_types:
                self.__bind()
            elif self.type in self.__connect_types:
                self.__connect()
            elif self.type == self.Type.helper:
                pass
            else:
                self.__unrecognized_connection_type()

        except ZMQError as ex:
            self.__error(ex)

        finally:
            if self.open:
                self.__ready()
            else:
                self.__not_connected()

    def __error(self, exception: ZMQError) -> None:
        self.open = False
        self.log.error(f"Error init socket for class {self}\nException -> {exception}")

    def __ready(self) -> None:
        self.log.debug(f'ready on channel ->{self.channel}')

    def __not_connected(self) -> None:
        self.log.warn(f'not connected on channel ->{self.channel}')

    def __unrecognized_connection_type(self) -> None:
        self.log.error(f'Zmq pattern not recognized {self.Type}')

    def __bind(self) -> None:
        self.socket.bind(self.channel())
        self.open = True
        self.log.debug(f'on channel {self.channel()}')

    def __connect(self) -> None:

        self.socket.connect(self.channel())
        if self.type is self.Type.subscriber:
            self.socket.setsockopt(SUBSCRIBE, b'')
        self.open = True
        self.log.debug(f'on channel {self.channel()}')

    def create_packet(self, data: object = None) -> Packet:
        """
        Create Packet

        :param: data: User Data
        :return: Packet

        """
        return Packet(sender=self.name, channel=self.channel(), data=data)

    def is_connection_open(self) -> bool:
        """
        Is the connection open

        :return: connection open

        """
        return self.open

    def close(self) -> None:
        """
        Close Connection
        """
        self.open = False
        self.socket.close()
        self.log.debug('Closed')


class ConnectionDataHandler(ConnectionBase):

    def decode(self, serialized_data: Union[bytes, ByteString]) -> Union[Any, Packet]:
        """
        Decode serialized data

        :param: serialized_data:
        :return: python object

        """
        res = None

        try:
            res = pickle.loads(serialized_data)  # type: ignore[arg-type]
        except pickle.UnpicklingError:
            # Try decompress
            decompress_bytes = self.decompress(serialized_data)
            self.log.warning('maybe the input is compressed. Try to decompress then decode again.')
            try:
                res = pickle.loads(decompress_bytes)
            except pickle.UnpicklingError as ex:
                print(f'Error Pickle -> {ex}')
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            return res

    def encode(self, obj: object, compression: bool = False) -> bytes:
        """
        Encode python object

        :param: obj: input target python object
        :param: compression: flag activate compression
        :return: encoded python object

        """
        res = None
        try:
            res = pickle.dumps(obj)
            if compression:
                res = self.compress(res)
        except pickle.UnpicklingError as ex:
            self.log.error(f'Error -> {ex}')
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            assert isinstance(res, bytes)
            return res

    def decompress(self, compress_byte: Any) -> Union[bytes, Any]:
        """
        Decompress input

        :param: compress_byte:
        :return: decompressed input

        """
        res = None
        try:
            res = blosc2.decompress(compress_byte)
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            return res

    def compress(self, byte: bytes) -> Any:
        """
        Compress input using zlib

        :param byte:
        :return: compressed input

        """
        res = None
        try:
            res = blosc2.compress(byte, cname='zlib')
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            return res

    def decode_packet(self, packet: Packet) -> Packet:
        """
        Decode Packet

        :param: packet: input packet
        :return: decoded packet

        """
        res = True
        try:
            if packet.compressed:
                # Decompress
                packet.data = self.decompress(packet.data)
                packet.compressed = False
            if packet.encoded:
                # Decode
                packet.data = self.decode(packet.data)  # type: ignore[arg-type]
                packet.encoded = False
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
            res = False
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            return packet

    def encode_packet(self, packet: Packet, data_encode: bool = True, data_compress: bool = True) -> Packet:
        """
        Encode Packet

        :param: packet: input packet
        :param: data_encode: flag encode data
        :param: data_compress: flag compress data
        :return: Encoded Packet

        """
        res = True
        try:
            if data_encode and not packet.encoded:
                # Encode Data
                packet.data = self.encode(packet.data)
                packet.encoded = True
            if data_compress and not packet.compressed:
                if not data_encode:
                    # Forcing Data Encode
                    packet.data = self.encode(packet.data)
                    packet.encoded = True
                # Compress Data
                packet.data = self.compress(packet.data)  # type: ignore[arg-type]
                packet.compressed = True
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
            res = False
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            return packet

    def hashing(self, bytes_obg: bytes) -> Union[str, None]:
        """
        Given the input return the relative hash

        :param: bytes_obg:
        :return: hash
        """
        res = None
        try:
            res = hashlib.md5(bytes_obg)
            res = res.hexdigest()  # type: ignore[assignment]
            assert isinstance(res, str)
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
        finally:
            if res:
                self.log.debug('success')
            else:
                self.log.error('failed')
            return res  # type: ignore[return-value]


class TryToUseConnectionTransmissionOnClosedConnection(Exception):
    pass


class ConnectionTransmission(ConnectionDataHandler):

    def safe_check(self) -> ConnectionTransmission:
        """
        Safe check before use any transmissions methods

        :return: self instance to concatenate methods

        """
        if self.open:
            return self
        else:
            raise TryToUseConnectionTransmissionOnClosedConnection

    def __receive(self) -> Union[Packet, object]:
        """
        Receive main internal method

        :return: received data

        """
        try:
            # Receive from the socket
            obj = self.decode(self.socket.recv())  # type: ignore[arg-type]
            self.log.debug(f"{obj}")
            return obj
        except ZMQError as ex:
            self.log.error(f"Error -> {ex}")
            return None

    def receive(self, raw: bool = False) -> Union[Packet, object]:
        """
        Receive method

        :param: raw: flag to receive data raw
        :return: received data

        """
        obj = self.safe_check().__receive()
        if raw:
            return obj
        else:
            if isinstance(obj, Packet):
                return self.decode_packet(obj)
            else:
                self.log.warning("Not a Packet received with raw set to False")
                return obj

    def __send(self, obj: object) -> bool:
        """
        Send main internal method

        :param: obj: target object to send
        :return: success or fail flag

        """
        try:
            self.log.debug(f"{obj}")
            self.socket.send(self.encode(obj))
            self.log.debug("success")
            return True
        except ZMQError as ex:
            self.log.error(f"failed. Error -> {ex}")
            return False

    def send(self, obj: object, as_packet: bool = True) -> bool:
        """
        Send method

        :param: obj: target object to send
        :param: as_packet: flag if needed the encapsulation in a Packet
        :return: success or fail flag

        """
        if as_packet and not isinstance(obj, Packet):
            # create packet with obj as data
            obj = self.create_packet(obj)

        return self.safe_check().__send(obj)


class Connection(ConnectionTransmission):
    pass
