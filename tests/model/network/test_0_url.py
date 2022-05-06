from pathlib import Path
from pynet.model.network.url import Url, LocalUrl, RemoteUrl, \
    DEFAULT_LOCAL_IP, DEFAULT_LOCAL_PORT, DEFAULT_LOCAL_SOCKET


def test_local_channel():
    lc = LocalUrl()
    assert lc.path == Path(DEFAULT_LOCAL_SOCKET)


def test_remote_channel():
    rc = RemoteUrl()
    assert rc.ip == DEFAULT_LOCAL_IP
    assert rc.port == DEFAULT_LOCAL_PORT


def test_channel():
    lc = Url().Local()
    assert lc.path == Path(DEFAULT_LOCAL_SOCKET)
    rc = Url().Remote()
    assert rc.ip == DEFAULT_LOCAL_IP
    assert rc.port == DEFAULT_LOCAL_PORT


def test_custom_channels():
    lc_path = Path('/tmp/test_1')
    lc = Url().Local(lc_path)
    assert lc.path == Path(lc_path)
    rc = Url().Remote('192.168.1.1', 22)
    assert rc.ip == '192.168.1.1'
    assert rc.port == 22
