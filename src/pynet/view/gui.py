from __future__ import annotations
import sys
import os
import time

import pkg_resources
from pathlib import Path
from PySide6.QtCore import QObject, Property, Signal, Slot, QUrl
from PySide6.QtGui import QGuiApplication, QSurfaceFormat
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import QQmlComponent
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication

from . import UI_LOGGER
from .controllers import Clock, Drop, LogMessage
from .. import __version__

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"


def get_root_qml_path() -> str:
    p = pkg_resources.resource_filename('pynet', 'view/ui/Main.qml')
    UI_LOGGER.log.debug(f'QML path: {p}')
    return p


def get_qml_component_path(cmp: str) -> QUrl:
    p = pkg_resources.resource_filename('pynet', f'view/ui/Components/{cmp}')
    UI_LOGGER.log.debug(f'Component QML {cmp} path: {p}')
    url = QUrl.fromLocalFile(p)
    UI_LOGGER.log.debug(f'Component QML {cmp} QUrl: {url}')
    return url


def construct_app() -> QGuiApplication:
    UI_LOGGER.log.debug('constructing application')
    return QGuiApplication(sys.argv)


def construct_formatter() -> QSurfaceFormat:
    UI_LOGGER.log.debug('constructing surface formatter')
    formatter = QSurfaceFormat()
    formatter.setSamples(8)
    QSurfaceFormat.setDefaultFormat(formatter)
    UI_LOGGER.log.debug('surface formatter set')
    return formatter


def construct_engine(app) -> QQmlApplicationEngine:
    UI_LOGGER.log.debug('constructing engine')
    engine = QQmlApplicationEngine()
    UI_LOGGER.log.debug('engine constructed')
    engine.quit.connect(app.quit)
    engine.load(get_root_qml_path())
    UI_LOGGER.log.debug('engine qml loaded')

    if not engine.rootObjects():
        UI_LOGGER.log.error('engine qml ERROR')
        sys.exit(-1)
    else:
        UI_LOGGER.log.debug('engine qml ok')

    return engine


def construct_controllers(engine) -> {QObject}:
    controllers = {
        'log': LogMessage(),
        'clock': Clock(),
        'drop': Drop()
    }
    # Assign controller to the engine
    root = engine.rootObjects()[0]
    # Set Controllers
    root.setProperty('logController', controllers['log'])
    root.setProperty('clockController', controllers['clock'])
    root.setProperty('dropController', controllers['drop'])
    # Set static Properties
    root.setProperty('appName', "PyNet")
    root.setProperty('appVersion', __version__)
    # Initial call to trigger first update. Must be after the setProperty to connect signals.
    controllers['clock'].update_time()
    UI_LOGGER.log.debug('controllers associated to the engine')
    return controllers, root


def construct_node(engine):
    component = QQmlComponent(engine)
    component.loadUrl(get_qml_component_path('Node.qml'))

    for err in component.errors():
        UI_LOGGER.log.error(f"Node component error: {err.toString()}")

    itm = None
    UI_LOGGER.log.debug(f'Component Status: {component.status()}')
    # get root (ApplicationWindow cast to QQuickItem)
    root_item = engine.rootObjects()[0].children()[0]
    if root_item:
        UI_LOGGER.log.debug(f'root has QQuickItem')
        print("CTX: ", engine.rootContext())
        itm = component.create(context=engine.rootContext())
        if itm:
            UI_LOGGER.log.debug(f'Node item created - parent: {itm.parent}')
            itm.setParent(root_item)
            UI_LOGGER.log.debug(f'Node assign parent: {itm.parent}, info: {itm.dumpObjectInfo()}')
        else:
            UI_LOGGER.log.error('Node qml not loaded')
    else:
        UI_LOGGER.log.error('Cannot get root has QQuickItem')
    return component, itm


def run():
    t_start = time.time_ns()

    formatter = construct_formatter()

    app = construct_app()
    engine = construct_engine(app)
    controllers, root = construct_controllers(engine)
    cmp, itm = construct_node(engine)
    controllers['log'].update_message(f'Ready in {int((time.time_ns() - t_start) * 1e-6)} ms')
    sys.exit(app.exec())
