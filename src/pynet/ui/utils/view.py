from PySide6.QtQuick import QQuickView
from .. import LOG


def new(parent, url, **kwargs):
    view = QQuickView()
    LOG.log.debug(f"setting source : {parent} / {url} ")
    view.setSource(url)
    ctx = view.rootContext()
    if ctx:
        LOG.log.debug(f"get root context ok")
        LOG.log.debug(f"context properties updated")
    else:
        LOG.log.error(f"get root context ok - abortion")

    return view
