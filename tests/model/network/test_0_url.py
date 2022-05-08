from pathlib import Path
import pytest
from pynet.model.network.url import Url, LocalUrl, RemoteUrl, \
    DEFAULT_LOCAL_IP, DEFAULT_LOCAL_PORT, DEFAULT_LOCAL_SOCKET


def test_local_bind_channel_default():
    lc = Url.Local()
    assert lc.path == Path(DEFAULT_LOCAL_SOCKET)


def test_remote_channel_default():
    rc = Url.Remote()
    assert rc.ip == DEFAULT_LOCAL_IP
    assert rc.port == DEFAULT_LOCAL_PORT


CUSTOM_PATH = Path('/tmp/test')


@pytest.mark.parametrize('local_type',
                         [Url.LocalType.ipc,
                          Url.LocalType.inproc,
                          ])
def test_local_channel_custom(local_type: Url.LocalType):
    lc = Url().Local(local_type=local_type, path=CUSTOM_PATH)
    assert lc.path == CUSTOM_PATH
    assert lc.local_type == local_type
    assert lc() == f'{local_type.name}://{CUSTOM_PATH}'


CUSTOM_IP = '192.168.1.1'
CUSTOM_PORT = 28


def test_remote_channel_custom():
    rc = Url().Remote(ip=CUSTOM_IP, port=CUSTOM_PORT)
    assert rc.ip == CUSTOM_IP
    assert rc.port == CUSTOM_PORT
    assert rc() == f"tcp://{str(CUSTOM_IP)}:{CUSTOM_PORT}"
