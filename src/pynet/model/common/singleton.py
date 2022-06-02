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
from typing import Dict


class Singleton(type):
    """

    Make any class as Singleton Class.

    Example Usage:
        >>> class ExampleClass(metaclass=Singleton)
    """
    _instances: Dict[object, object] = {}

    def __call__(cls: Singleton, *args: object, **kwargs: object) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
