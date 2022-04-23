import blosc2
import pickle
import hashlib
from typing import Any, Union


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
    def decompress(compress_byte: Any) -> Union[bytes, Any]:
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
    def decode(encoded_byte: bytes) -> object:
        """
        Deserialize input

        :param: encoded_byte:
        :return: python object deserialized

        """
        try:
            res = pickle.loads(encoded_byte)
        except pickle.UnpicklingError:
            # Try decompress
            decompress_bytes = Manipulator.decompress(encoded_byte)
            try:
                res = pickle.loads(decompress_bytes)
            except pickle.UnpicklingError as ex:
                print(f'Error Pickle -> {ex}')
                res = None
        return res
