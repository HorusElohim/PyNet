from pynet.model.network.sock import Sock
from pynet.model import Logger
import pytest
from time import sleep

TEST_1_SOCK_LOG = Logger('test_1_sock')


@pytest.mark.parametrize(
    'sock_url, pattern_type',
    [
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.publisher),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.subscriber),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.pusher),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.puller),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.requester),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.replier),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.INPROC), Sock.Pattern.pair),

        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.publisher),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.subscriber),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.pusher),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.puller),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.requester),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.replier),
        (Sock.SockUrl.Local(Sock.SockUrl.CLIENT, local_type=Sock.SockUrl.IPC), Sock.Pattern.pair),

        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.publisher),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.subscriber),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.pusher),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.puller),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.requester),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.replier),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.INPROC), Sock.Pattern.pair),

        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.publisher),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.subscriber),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.pusher),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.puller),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.requester),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.replier),
        (Sock.SockUrl.Local(Sock.SockUrl.SERVER, local_type=Sock.SockUrl.IPC), Sock.Pattern.pair),

    ])
def test_connection_open_close_single_local_sock_url(sock_url, pattern_type):
    sock = Sock('TestConnection', pattern_type, logger_other=TEST_1_SOCK_LOG)
    sock.sock_urls = sock_url
    assert sock.sock_urls[0] == sock_url
    assert sock._sock_pattern_type == pattern_type
    assert not sock.is_open
    sock.open()
    assert sock.is_open
    sock.close()
    assert not sock.is_open
    sleep(0.05)


@pytest.mark.parametrize(
    'sock_url, pattern_type',
    [
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.publisher),
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.subscriber),
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.pusher),
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.puller),
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.requester),
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.replier),
        (Sock.SockUrl.Remote(Sock.SockUrl.CLIENT), Sock.Pattern.pair),

        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.publisher),
        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.subscriber),
        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.pusher),
        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.puller),
        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.requester),
        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.replier),
        (Sock.SockUrl.Remote(Sock.SockUrl.SERVER), Sock.Pattern.pair),

    ])
def test_connection_open_close_single_remote_sock_url(sock_url, pattern_type):
    sock = Sock('TestConnection', pattern_type, logger_other=TEST_1_SOCK_LOG)
    sock.sock_urls = sock_url
    assert sock.sock_urls[0] == sock_url
    assert sock._sock_pattern_type == pattern_type
    assert not sock.is_open
    sock.open()
    assert sock.is_open
    sock.close()
    assert not sock.is_open
    sleep(0.05)
