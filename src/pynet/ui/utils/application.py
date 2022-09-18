from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from .. import LOG


def new(*args, **kwargs):
    LOG.log.debug("QtWidget::QApplication - ")
    app = QApplication(*args, **kwargs)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    LOG.log.debug("QtWidget::QApplication - New")
    return app
