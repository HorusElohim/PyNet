from pynet.model.network import LocalChannel, RemoteChannel
from pynet.model.network.data.channel import DEFAULT_LOCAL_IP, DEFAULT_LOCAL_PORT, DEFAULT_LOCAL_SOCKET
from pathlib import Path


def test_local_chanel():
    lc = LocalChannel()
    assert lc.path == Path(DEFAULT_LOCAL_SOCKET)


def test_remote_chanel():
    lc = RemoteChannel()
    assert lc.ip == DEFAULT_LOCAL_IP
    assert lc.port == DEFAULT_LOCAL_PORT
