from pynet.ui import application, qml, view, engine, vm
from pynet import __version__
import sys


def run():
    pynet_app = application.new()
    pynet_vm = vm.ViewModel(parent=pynet_app)

    pynet_engine = engine.new()
    engine.add_property(pynet_engine, 'appName', 'PyNet')
    engine.add_property(pynet_engine, 'appVersion', __version__)
    engine.add_property(pynet_engine, 'appVm', pynet_vm)
    pynet_vm.get_clock().update_time()
    engine.load_qml(pynet_engine, qml.url('ui/qml/UI.qml'))
    pynet_engine.quit.connect(pynet_app.quit)

    sys.exit(pynet_app.exec())


if __name__ == "__main__":
    run()
