from __future__ import annotations
from typing import Dict


class Singleton(type):
    _instances: Dict[object, object] = {}

    def __call__(cls: Singleton, *args: object, **kwargs: object) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
