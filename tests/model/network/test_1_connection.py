from pynet.model.network.core import Core, CoreType
from pynet.model.network.connection import Connection
from pynet.model.network.url import Url
import pytest
from zmq import Context
from time import sleep


@pytest.mark.parametrize(
    'connection_type , pattern_type, local_type',
    [(Connection.Type.bind, Connection.Pattern.publisher, Url.LocalType.inproc),
     (Connection.Type.bind, Connection.Pattern.subscriber, Url.LocalType.inproc),
     (Connection.Type.bind, Connection.Pattern.pusher, Url.LocalType.inproc),
     (Connection.Type.bind, Connection.Pattern.puller, Url.LocalType.inproc),
     (Connection.Type.bind, Connection.Pattern.replier, Url.LocalType.inproc),
     (Connection.Type.bind, Connection.Pattern.requester, Url.LocalType.inproc),

     (Connection.Type.connect, Connection.Pattern.publisher, Url.LocalType.inproc),
     (Connection.Type.connect, Connection.Pattern.subscriber, Url.LocalType.inproc),
     (Connection.Type.connect, Connection.Pattern.pusher, Url.LocalType.inproc),
     (Connection.Type.connect, Connection.Pattern.puller, Url.LocalType.inproc),
     (Connection.Type.connect, Connection.Pattern.replier, Url.LocalType.inproc),
     (Connection.Type.connect, Connection.Pattern.requester, Url.LocalType.inproc),
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
    [(Connection.Type.bind, Connection.Pattern.publisher),
     (Connection.Type.bind, Connection.Pattern.subscriber),
     (Connection.Type.bind, Connection.Pattern.pusher),
     (Connection.Type.bind, Connection.Pattern.puller),
     (Connection.Type.bind, Connection.Pattern.replier),
     (Connection.Type.bind, Connection.Pattern.requester),

     (Connection.Type.connect, Connection.Pattern.publisher),
     (Connection.Type.connect, Connection.Pattern.subscriber),
     (Connection.Type.connect, Connection.Pattern.pusher),
     (Connection.Type.connect, Connection.Pattern.puller),
     (Connection.Type.connect, Connection.Pattern.replier),
     (Connection.Type.connect, Connection.Pattern.requester),
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
    con = Connection('TestConnection', Connection.Type.connect, Connection.Pattern.publisher)
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
