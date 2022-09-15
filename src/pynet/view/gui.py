import sys
import os
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from .backend import Backend
from . import UI_LOGGER
import pkg_resources

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"


def get_qml_path() -> str:
    return pkg_resources.resource_filename('pynet', 'view/ui/Main.qml')


UI_LOGGER.log.debug(f'QML path: {get_qml_path()}')


def construct_app() -> QGuiApplication:
    UI_LOGGER.log.debug('constructing application')
    return QGuiApplication(sys.argv)


def construct_engine(app) -> QQmlApplicationEngine:
    UI_LOGGER.log.debug('constructing engine')
    engine = QQmlApplicationEngine()
    UI_LOGGER.log.debug('engine constructed')
    engine.quit.connect(app.quit)
    engine.load(get_qml_path())
    UI_LOGGER.log.debug('engine qml loaded')

    if not engine.rootObjects():
        UI_LOGGER.log.error('engine qml ERROR')
        sys.exit(-1)
    else:
        UI_LOGGER.log.debug('engine qml ok')

    return engine


def construct_backend(engine) -> Backend:
    backend = Backend()
    engine.rootObjects()[0].setProperty('backend', backend)
    UI_LOGGER.log.debug('backed associated to the engine')
    return backend


def run():
    app = construct_app()
    engine = construct_engine(app)
    backend = construct_backend(engine)
    # Initial call to trigger first update. Must be after the setProperty to connect signals.
    backend.update_time()
    sys.exit(app.exec())
