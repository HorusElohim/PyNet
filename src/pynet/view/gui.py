import sys
import os
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from .backend import Backend
from . import UI_LOGGER
import pkg_resources

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    UI_LOGGER.log.debug(f'QML PyInstaller base-path : {base_path}')
    UI_LOGGER.log.debug(f'QML PyInstaller content : {list(Path(base_path).iterdir())}')
    return Path(Path(base_path) / relative_path).absolute()


def get_qml_path() -> str:
    # return str(Path(Path(__file__).parent / 'ui' / 'Main.qml').absolute())
    return pkg_resources.resource_filename('pynet', 'view/ui/Main.qml')


UI_LOGGER.log.debug(f'QML path: {get_qml_path()}')
UI_LOGGER.log.debug(f'QML PyInstaller path: {resource_path("ui/Main.qml")}')


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
