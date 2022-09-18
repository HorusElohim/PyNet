import pkg_resources
from PySide6.QtCore import QUrl


def url(qml_file: [str]):
    return QUrl.fromLocalFile(pkg_resources.resource_filename('pynet', qml_file))
