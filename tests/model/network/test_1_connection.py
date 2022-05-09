from pynet.model.network.connection import Connection
from pynet.model.network.url import Url
import pytest
from zmq import Context
from time import sleep


@pytest.mark.parametrize(
    'connection_type , pattern_type, local_type',
    [
        (Connection.SERVER, Connection.PUB, Url.INPROC),
        (Connection.SERVER, Connection.SUB, Url.INPROC),
        (Connection.SERVER, Connection.PUSH, Url.INPROC),
        (Connection.SERVER, Connection.PULL, Url.INPROC),
        (Connection.SERVER, Connection.REP, Url.INPROC),
        (Connection.SERVER, Connection.REQ, Url.INPROC),
        (Connection.SERVER, Connection.PAIR, Url.INPROC),

        (Connection.CLIENT, Connection.PUB, Url.INPROC),
        (Connection.CLIENT, Connection.SUB, Url.INPROC),
        (Connection.CLIENT, Connection.PUSH, Url.INPROC),
        (Connection.CLIENT, Connection.PULL, Url.INPROC),
        (Connection.CLIENT, Connection.REP, Url.INPROC),
        (Connection.CLIENT, Connection.REQ, Url.INPROC),
        (Connection.CLIENT, Connection.PAIR, Url.INPROC),

        (Connection.SERVER, Connection.PUB, Url.IPC),
        (Connection.SERVER, Connection.SUB, Url.IPC),
        (Connection.SERVER, Connection.PUSH, Url.IPC),
        (Connection.SERVER, Connection.PULL, Url.IPC),
        (Connection.SERVER, Connection.REP, Url.IPC),
        (Connection.SERVER, Connection.REQ, Url.IPC),
        (Connection.SERVER, Connection.PAIR, Url.IPC),

        (Connection.CLIENT, Connection.PUB, Url.IPC),
        (Connection.CLIENT, Connection.SUB, Url.IPC),
        (Connection.CLIENT, Connection.PUSH, Url.IPC),
        (Connection.CLIENT, Connection.PULL, Url.IPC),
        (Connection.CLIENT, Connection.REP, Url.IPC),
        (Connection.CLIENT, Connection.REQ, Url.IPC),
        (Connection.CLIENT, Connection.PAIR, Url.IPC),
    ])
def test_connection_local_open_close(connection_type, pattern_type, local_type):
    con = Connection('TestConnection', connection_type, pattern_type)
    assert con._connection_type == connection_type
    assert con._connection_pattern_type == pattern_type
    # Add Url
    con.url = Url.Local(local_type=local_type)
    assert not con.is_open
    con.open()
    assert con.is_open
    con.close()
    assert not con.is_open
    sleep(0.1)


@pytest.mark.parametrize(
    'connection_type , pattern_type',
    [(Connection.SERVER, Connection.PUB),
     (Connection.SERVER, Connection.SUB),
     (Connection.SERVER, Connection.PUSH),
     (Connection.SERVER, Connection.PULL),
     (Connection.SERVER, Connection.REP),
     (Connection.SERVER, Connection.REQ),
     (Connection.SERVER, Connection.PAIR),

     (Connection.CLIENT, Connection.PUB),
     (Connection.CLIENT, Connection.SUB),
     (Connection.CLIENT, Connection.PUSH),
     (Connection.CLIENT, Connection.PULL),
     (Connection.CLIENT, Connection.REP),
     (Connection.CLIENT, Connection.REQ),
     (Connection.CLIENT, Connection.PAIR),
     ])
def test_connection_remote_open_close(connection_type, pattern_type):
    con = Connection('TestConnection', connection_type, pattern_type)
    assert con._connection_type == connection_type
    assert con._connection_pattern_type == pattern_type
    # Add Url
    con.url = Url.Remote()
    assert not con.is_open
    con.open()
    assert con.is_open
    con.close()
    assert not con.is_open


def test_connection_multiple():
    con = Connection('TestConnection', Connection.CLIENT, Connection.SUB)
    # Add Url
    con.url = Url.Remote()
    con.url = Url.Remote(port=29129)
    con.url = Url.Remote(port=29130)
    con.url = Url.Remote(port=29131)
    assert not con.is_open
    con.open()
    assert con.is_open
    con.close()
    assert not con.is_open
