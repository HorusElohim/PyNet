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
