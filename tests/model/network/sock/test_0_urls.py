from pathlib import Path
import pytest
from pynet.model.network import SockUrl


def test_local_sock_url_default():
    lc = SockUrl.Local(SockUrl.SERVER)
    assert lc.sock_type == SockUrl.SERVER
    assert lc.path == Path('/tmp/pynet_0')
    assert lc.local_type == SockUrl.LocalType.inproc


def test_remote_sock_url_default():
    rc = SockUrl.Remote(SockUrl.SERVER)
    assert rc.sock_type == SockUrl.SERVER
    assert rc.ip == '127.0.0.1'
    assert rc.port == 28128


CUSTOM_PATH = Path('/tmp/test')


@pytest.mark.parametrize('local_type',
                         [SockUrl.IPC,
                          SockUrl.INPROC,
                          ])
def test_local_sock_urls_custom(local_type: SockUrl.LocalType):
    lc = SockUrl().Local(SockUrl.SERVER, local_type=local_type, path=CUSTOM_PATH)
    assert lc.sock_type == SockUrl.SERVER
    assert lc.path == CUSTOM_PATH
    assert lc.local_type == local_type
    assert lc() == f'{local_type.name}://{CUSTOM_PATH}'


CUSTOM_IP = '192.168.1.1'
CUSTOM_PORT = 28


def test_remote_sock_urls_custom():
    rc = SockUrl().Remote(SockUrl.SERVER, ip=CUSTOM_IP, port=CUSTOM_PORT)
    assert rc.sock_type == SockUrl.SERVER
    assert rc.ip == CUSTOM_IP
    assert rc.port == CUSTOM_PORT
    assert rc() == f"tcp://{str(CUSTOM_IP)}:{CUSTOM_PORT}"
