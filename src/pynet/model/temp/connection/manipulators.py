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
from . import ConnectionBase
from ...common import Singleton, Logger


class ManipulatorLogger(Logger):
    pass


M_LOGGER = ManipulatorLogger()


class Deserializer:
    @classmethod
    def decode(cls, serialized_data: Union[bytes, ByteString]) -> Union[Any, Packet]:
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
            decompress_bytes = cls.decompress(serialized_data)
            M_LOGGER.log.warning('maybe the input is compressed. Try to decompress then decode again.')
            try:
                res = pickle.loads(decompress_bytes)
            except pickle.UnpicklingError as ex:
                print(f'Error Pickle -> {ex}')
        finally:
            if res:
                M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
            else:
                M_LOGGER.log.error(f'{cls.__class__.__name__}::failed')
            return res


class Serializer:
    @classmethod
    def encode(cls, obj: object, compression: bool = False) -> bytes:
        """
        Encode python object

        :param: obj: input target python object
        :param: compression: flag activate compression
        :return: encoded python object

        """
        res = None
        try:
            M_LOGGER.log.debug(f'{cls.__class__.__name__}::input: {obj}')
            res = pickle.dumps(obj)
            M_LOGGER.log.debug(f'{cls.__class__.__name__}::res: {res}')
            if compression:
                res = cls.compress(res)
            if res:
                M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
            else:
                M_LOGGER.log.error(f'{cls.__class__.__name__}::failed {res}')
                return res
        except pickle.UnpicklingError as ex:
            M_LOGGER.log.error(f'{cls.__class__.__name__}::Error -> {ex}')
            return bytes()


class Decompressor:
    @classmethod
    def decompress(cls, compress_byte: Any) -> Union[bytes, Any]:
        """
        Decompress input

        :param: compress_byte:
        :return: decompressed input

        """
        res = None
        try:
            res = blosc2.decompress(compress_byte)
            if res:
                M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
            else:
                M_LOGGER.log.error(f'{cls.__class__.__name__}::failed')
            return res
        except Exception as ex:
            M_LOGGER.log.error(f'{cls.__class__.__name__}::Error -> {ex}')
            return None


class Compressor:
    @classmethod
    def compress(cls, byte: bytes) -> Any:
        """
        Compress input using zlib

        :param byte:
        :return: compressed input

        """
        res = None
        try:
            M_LOGGER.log.debug(f'{cls.__class__.__name__}::input: {byte}')
            res = blosc2.compress(byte, cname='zlib')
        except Exception as ex:
            M_LOGGER.log.error(f'{cls.__class__.__name__}::Error -> {ex}')
        finally:
            if res:
                M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
            else:
                M_LOGGER.log.error(f'{cls.__class__.__name__}::failed')
            return res

    # def decode_packet(cls, packet: Packet) -> Packet:
    #     """
    #     Decode Packet
    #
    #     :param: packet: input packet
    #     :return: decoded packet
    #
    #     """
    #     res = True
    #     try:
    #         if packet.compressed:
    #             # Decompress
    #             packet.data = cls.decompress(packet.data)
    #             packet.compressed = False
    #         if packet.encoded:
    #             # Decode
    #             packet.data = cls.decode(packet.data)  # type: ignore[arg-type]
    #             packet.encoded = False
    #     except Exception as ex:
    #         M_LOGGER.log.error(f'{cls.__class__.__name__}::Error -> {ex}')
    #         res = False
    #     finally:
    #         if res:
    #             M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
    #         else:
    #             M_LOGGER.log.error(f'{cls.__class__.__name__}::failed')
    #         return packet
    #
    # def encode_packet(cls, packet: Packet, data_encode: bool = True, data_compress: bool = True) -> Packet:
    #     """
    #     Encode Packet
    #
    #     :param: packet: input packet
    #     :param: data_encode: flag encode data
    #     :param: data_compress: flag compress data
    #     :return: Encoded Packet
    #
    #     """
    #     res = True
    #     try:
    #         if data_encode and not packet.encoded:
    #             # Encode Data
    #             packet.data = cls.encode(packet.data)
    #             packet.encoded = True
    #         if data_compress and not packet.compressed:
    #             if not data_encode:
    #                 # Forcing Data Encode
    #                 packet.data = cls.encode(packet.data)
    #                 packet.encoded = True
    #             # Compress Data
    #             packet.data = cls.compress(packet.data)  # type: ignore[arg-type]
    #             packet.compressed = True
    #     except Exception as ex:
    #         M_LOGGER.log.error(f'{cls.__class__.__name__}::Error -> {ex}')
    #         res = False
    #     finally:
    #         if res:
    #             M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
    #         else:
    #             M_LOGGER.log.error(f'{cls.__class__.__name__}::failed')
    #         return packet


class Hasher:
    @classmethod
    def hashing(cls, bytes_obg: bytes) -> Union[str, None]:
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
            M_LOGGER.log.error(f'{cls.__class__.__name__}::Error -> {ex}')
        finally:
            if res:
                M_LOGGER.log.debug(f'{cls.__class__.__name__}::success')
            else:
                M_LOGGER.log.error(f'{cls.__class__.__name__}::failed')
            return res  # type: ignore[return-value]
