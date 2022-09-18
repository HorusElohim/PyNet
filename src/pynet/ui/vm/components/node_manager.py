from PySide6.QtCore import Property, QObject, Qt
from PySide6.QtGui import QColor, QGuiApplication, QStandardItem, QStandardItemModel


class NodeManager(QObject):
    def __init__(self, parent=None):
        super(NodeManager, self).__init__(parent)
        self._model = QStandardItemModel
        # self._model.setItemRoleNames()
