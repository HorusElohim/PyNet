from PySide6.QtCore import QObject
from ....utils import Property, PropertyMeta


class Card(QObject, metaclass=PropertyMeta):
    image = Property('')
    color = Property('white')
    visible_body = Property(True)
