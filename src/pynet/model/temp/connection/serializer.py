# Copyright (C) 2022 HorusElohim
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from typing import Union, Any, ByteString
import hashlib
import blosc2
import pickle

from .. import Packet
from ...common import Singleton, Logger


class Serializer(metaclass=Singleton, Logger):

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
                self.log.debug(f'success')
            else:
                self.log.error(f'failed')
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
            self.log.debug(f'input: {obj}')
            res = pickle.dumps(obj)
            self.log.debug(f'res: {res}')
            if compression:
                res = self.compress(res)
            if res:
                self.log.debug(f'success')
            else:
                self.log.error(f'failed {res}')
                return res
        except pickle.UnpicklingError as ex:
            self.log.error(f'Error -> {ex}')
            return bytes()

    def decompress(self, compress_byte: Any) -> Union[bytes, Any]:
        """
        Decompress input

        :param: compress_byte:
        :return: decompressed input

        """
        res = None
        try:
            res = blosc2.decompress(compress_byte)
            if res:
                self.log.debug(f'success')
            else:
                self.log.error(f'failed')
            return res
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
            return None

    def compress(self, byte: bytes) -> Any:
        """
        Compress input using zlib

        :param byte:
        :return: compressed input

        """
        res = None
        try:
            self.log.debug(f'input: {byte}')
            res = blosc2.compress(byte, cname='zlib')
        except Exception as ex:
            self.log.error(f'Error -> {ex}')
        finally:
            if res:
                self.log.debug(f'success')
            else:
                self.log.error(f'failed')
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
                self.log.debug(f'success')
            else:
                self.log.error(f'failed')
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
                self.log.debug(f'success')
            else:
                self.log.error(f'failed')
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
                self.log.debug(f'success')
            else:
                self.log.error(f'failed')
            return res  # type: ignore[return-value]
