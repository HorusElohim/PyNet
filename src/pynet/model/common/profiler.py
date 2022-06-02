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


import time
from typing import Any
from . import Logger


def profile(method: Any) -> Any:
    """
    Profile Decorator
    :param method:
    :return:

    Examples:
        >>> @profile
        >>> def test_function():
        >>>     pass
        profiler.py:11 in profile_decorator     DEBUG           test_function took 0.01 ms

    """

    def profile_decorator(*args: object, **kw: object) -> Any:
        ts = time.time_ns()
        result = method(*args, **kw)
        e_time = time.time_ns() - ts
        logger = Logger()
        logger.log.debug(f'{method.__name__} took {e_time * 1e-6} ms')
        return result

    return profile_decorator
