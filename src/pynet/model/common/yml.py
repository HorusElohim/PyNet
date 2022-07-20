# -*- coding: utf-8 -*-
from __future__ import annotations
from .ddict import DDict
from pathlib import Path
import yaml as yml
from typing import Dict, Any


class YmlSaveParentFolderDoNotExist(Exception):
    pass


class YmlLoadFileDoNotExist(Exception):
    pass


class Yml:
    @staticmethod
    def load(path: Path, ns: str = '') -> DDict | None:
        if not path.exists():
            raise YmlLoadFileDoNotExist
        with open(path, 'r') as fd:
            data = DDict(yml.safe_load(fd.read()))
        if ns:
            data = data[ns]
        return data

    @staticmethod
    def save(path: Path, data: DDict | Dict[Any, Any]) -> None:  # type: ignore
        if not path.parent.exists():
            raise YmlSaveParentFolderDoNotExist
        with open(path, 'w') as fd:
            yml.dump(data, fd)
