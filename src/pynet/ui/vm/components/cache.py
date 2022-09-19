from __future__ import annotations

from PySide6.QtCore import QObject
from pathlib import Path

from pynet import RUN_PATH, DDict
from pynet.model import Yml

from dataclasses import dataclass

from ... import LOG


class Cache:
    def __init__(self, name):
        LOG.log.debug(f"new cache: {name}")
        self.name = name
        self.path = RUN_PATH / 'cache' / name
        self.data = DDict()
        restored = self.load()
        LOG.log.debug(f"cache restored {restored} : {self.data}")

    def load(self) -> bool:
        LOG.log.debug(f'cache load - {self.path}')
        self.data = Yml.load(self.path)
        if len(self.data) > 1:
            return True
        return False

    def save(self):
        LOG.log.debug(f'cache save - {self.path} ')
        Yml.save(self.path, self.data)
        return self

    def get(self, key):
        if key in self.data:
            LOG.log.debug(f'cache {key}: loaded')
            return self.data[key]
        else:
            LOG.log.warning(f'cache {key}: NOT loaded')
        return '-'
