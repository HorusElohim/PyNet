import blosc2
import pickle
import hashlib
from typing import Any


class Manipulator:

    @staticmethod
    def compress(byte: bytes) -> Any:
        """
        Compress input using zlib

        :param byte:
        :return: compressed input

        """
        return blosc2.compress(byte, cname='zlib')

    @staticmethod
    def decompress(compress_byte: Any) -> Any:
        """
        Decompress input

        :param: compress_byte:
        :return: decompressed input

        """
        return blosc2.decompress(compress_byte)

    @staticmethod
    def hashing(bytes_obg: bytes) -> str:
        """
        Given the input return the relative hash

        :param: bytes_obg:
        :return: hash
        """
        md5 = hashlib.md5(bytes_obg)
        return md5.hexdigest()

    @staticmethod
    def encode(obj: object) -> bytes:
        """
        Serialize the input object using pickle

        :param: obj:
        :return: serialized input

        """
        return pickle.dumps(obj)

    @staticmethod
    def decode(compress_byte: bytes) -> object:
        """
        Deserialize input

        :param: compress_byte:
        :return: python object deserialized

        """
        return pickle.loads(compress_byte)
