from . import Logger, Any


class AbcEntity(Logger):
    def __init__(self, entity_name: str, *args: Any, **kwargs: Any) -> None:
        self.entity_name = entity_name
        Logger.__init__(self, entity_name, **kwargs)
