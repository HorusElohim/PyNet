from __future__ import annotations

from .singleton import Singleton
from .ddict import DDict
from .yml import Yml
from .time import now, now_lite, today, delta_millisecond
from .logger import Logger, LoggerLevel, LoggerCannotWorkIfBothConsoleAndFileAreDisabled
from .size import Size
from .profiler import profile
from .process import Process

from typing import Any
import hashlib
import blosc2
import pickle


def compress(byte: bytes) -> Any:
    return blosc2.compress(byte, cname='zlib')


def decompress(compress_byte: bytes) -> Any:
    return blosc2.decompress(compress_byte)


def hexhashing(obj: bytes | object | list[object]) -> int:
    if isinstance(obj, list):
        return incremental_hexhashing(obj)
    return oneshot_hexhashing(obj)


def oneshot_hexhashing(obj: bytes | object) -> int:
    if not isinstance(obj, bytes):
        obj = pickle.dumps(obj)
    md5 = hashlib.md5(obj)
    return int(md5.hexdigest(), 16)


def oneshot_str_hexhashing(txt: str) -> int:
    return oneshot_hexhashing(txt.encode('utf-8'))


def incremental_hexhashing(sequence: list[object]) -> int:
    md5 = hashlib.md5()
    for x in sequence:
        md5.update(pickle.dumps(x))
    return int(md5.hexdigest(), 16)


def encode(obj: object) -> bytes:
    return pickle.dumps(obj)


def decode(compress_byte: bytes) -> object:
    return pickle.loads(compress_byte)
