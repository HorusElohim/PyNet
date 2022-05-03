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


from __future__ import annotations
from dataclassy import dataclass
import time

from ..common import Size


@dataclass(unsafe_hash=True, slots=True)
class PacketBase:
    """
        PacketBase Class
            Addition Packet Information
    """

    sender: str
    encoded: bool = False
    compressed: bool = False
    sequence_left: int = 0
    time: int = 0

    def __init__(self, sender: str, sequence_left: int = 0):
        """

        :param sender: Sender name
        :param sequence_left: Sequence Packet left to send

        """
        self.sender = sender
        self.encoded = False
        self.compressed = False
        self.sequence_left = sequence_left
        self.time = time.time_ns()

    def __repr__(self) -> str:
        return f'<Packet, {self.sender}, compressed:{self.compressed},' \
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

    def __init__(self, sender: str, data: object, sequence_left: int = 0):
        super().__init__(sender, sequence_left)
        self.data = data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.sender == other.sender and self.data == other.data
        return False
