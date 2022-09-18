from pynet.ui import application, qml, engine, vm
import time
import sys


def run():
    t_start = time.time_ns()
    pynet_app = application.new()
    pynet_vm = vm.ViewModel(parent=pynet_app)
    pynet_engine = engine.new()
    pynet_engine.quit.connect(pynet_app.quit)
    engine.add_property(pynet_engine, 'appVm', pynet_vm)
    engine.load_qml(pynet_engine, qml.url('ui/qml/UI.qml'))
    pynet_vm._upnp_client.start_discovery()
    pynet_vm.log_message(f'Ready in {int((time.time_ns() - t_start) * 1e-6)} ms')
    sys.exit(pynet_app.exec())


if __name__ == "__main__":
    run()
