from .base import ConnectionBase
from .manipulators import Serializer, Deserializer, Compressor, Decompressor
from .transmission import ConnectionTransmission


class Connection(ConnectionTransmission):
    pass
