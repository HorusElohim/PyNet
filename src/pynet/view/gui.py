import sys
import os
import pkg_resources
from PySide6.QtCore import QObject
from PySide6.QtGui import QGuiApplication, QSurfaceFormat
from PySide6.QtQml import QQmlApplicationEngine
from . import UI_LOGGER
from .controllers.clock import Clock
from .controllers.drop import Drop

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"


def get_qml_path() -> str:
    return pkg_resources.resource_filename('pynet', 'view/ui/Main.qml')


UI_LOGGER.log.debug(f'QML path: {get_qml_path()}')


def construct_app() -> QGuiApplication:
    UI_LOGGER.log.debug('constructing application')
    return QGuiApplication(sys.argv)


def construct_formatter() -> QSurfaceFormat:
    UI_LOGGER.log.debug('constructing surface formatter')
    formatter = QSurfaceFormat()
    formatter.setSamples(8)
    QSurfaceFormat.setDefaultFormat(formatter)
    UI_LOGGER.log.debug('surface formatter set')


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


def construct_controllers(engine) -> {QObject}:
    controllers = {
        'clock': Clock(),
        'drop': Drop()
    }
    # Assign controller to the engine
    engine.rootObjects()[0].setProperty('clockController', controllers['clock'])
    engine.rootObjects()[0].setProperty('dropController', controllers['drop'])
    # Initial call to trigger first update. Must be after the setProperty to connect signals.
    controllers['clock'].update_time()
    UI_LOGGER.log.debug('controllers associated to the engine')
    return controllers


def run():
    app = construct_app()
    engine = construct_engine(app)
    formatter = construct_formatter()
    controllers = construct_controllers(engine)
    sys.exit(app.exec())
