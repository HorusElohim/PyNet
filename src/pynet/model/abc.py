from . import Logger


class AbcEntity(Logger):
    def __init__(self, entity_name: str, *args, **kwargs):
        self.entity_name = entity_name
        Logger.__init__(self, entity_name, **kwargs)

