from __future__ import annotations
from dataclassy import dataclass
import time

from ...common import Size


@dataclass(unsafe_hash=True, slots=True)
class PacketBase:
    """
        PacketBase Class
            Addition Packet Information
    """

    sender: str
    encoded: bool = False
    compressed: bool = False
    channel: str = 'Unset'
    sequence_left: int = 0
    time: int = 0

    def __init__(self, sender: str, channel: str, sequence_left: int = 0):
        """

        :param sender: Sender name
        :param channel: Target Channel
        :param sequence_left: Sequence Packet left to send

        """
        self.sender = sender
        self.channel = channel
        self.encoded = False
        self.compressed = False
        self.sequence_left = sequence_left
        self.time = time.time_ns()

    def __repr__(self) -> str:
        return f'<Packet, {self.sender}, {self.channel}, compressed:{self.compressed},' \
               f' seq_left:{self.sequence_left}, age:{self.age:.4f} ms>'

    @property
    def size(self) -> str:
        return Size.pretty_obj_size(self)

    @property
    def age(self) -> float:
        return (time.time_ns() - self.time) * 1e-6


class Packet(PacketBase):
    """
        Packet Class
            The data is encapsulated inside this class
            with additional information

    """
    data: object = None

    def __init__(self, sender: str, channel: str, data: object, sequence_left: int = 0):
        super().__init__(sender, channel, sequence_left)
        self.data = data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.channel == other.channel and self.data == other.data
        return False
