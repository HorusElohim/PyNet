from __future__ import annotations

from pynet import RUN_PATH, DDict
from pynet.model import Yml

from .. import LOG


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
        LOG.log.debug(f'saving cache to {self.path} : {self.data} ')
        Yml.save(self.path, self.data.copy())
        return self

    def get(self, key, default="-"):
        if self.has(key):
            LOG.log.debug(f'cache {key}: loaded')
            return self.data[key]
        else:
            LOG.log.warning(f'cache {key}: NOT loaded')
        return default

    def has(self, key):
        if key in self.data:
            return True
        return False
