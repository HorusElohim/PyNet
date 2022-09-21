from __future__ import annotations

from ... import RUN_PATH
from .. import AbcEntity, Yml, DDict


class Cache(AbcEntity):
    def __init__(self, name, **kwargs):
        AbcEntity.__init__(self, entity_name=name, **kwargs)
        self.log.debug(f"new cache: {name}")
        self.name = name
        self.path = RUN_PATH / 'cache' / name
        self.data = DDict()
        restored = self.load()
        self.log.debug(f"cache restored {restored} : {self.data}")

    def load(self) -> bool:
        self.log.debug(f'cache load - {self.path}')
        self.data = Yml.load(self.path)
        if len(self.data) > 1:
            return True
        return False

    def save(self):
        self.log.debug(f'saving cache to {self.path} : {self.data} ')
        Yml.save(self.path, self.data.copy())
        return self

    def get(self, key, default="-"):
        if self.has(key):
            self.log.debug(f'cache {key}: loaded')
            return self.data[key]
        else:
            self.log.warning(f'cache {key}: NOT loaded')
        return default

    def has(self, key):
        if key in self.data:
            return True
        return False
