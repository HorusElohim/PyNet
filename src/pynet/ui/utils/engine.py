import sys
from PySide6.QtQml import QQmlApplicationEngine
from .. import LOG


def new():
    engine = QQmlApplicationEngine()
    LOG.log.debug('engine New')
    return engine


def load_qml(engine, root_qml: str):
    engine.load(root_qml)
    if not engine.rootObjects():
        LOG.log.error('engine qml ERROR')
        sys.exit(-1)
    else:
        LOG.log.debug('engine qml ok')


def add_property(engine, name, value):
    ctx = engine.rootContext()
    ctx.setContextProperty(name, value)
    LOG.log.debug(f"context add_property: [{name}/{value}]")
