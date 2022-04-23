from pynet.model.network import Connection, LocalChannel

CHANNEL = LocalChannel()


def test_connection_pub():
    conn_type = Connection.Type.publisher
    c = Connection('test', conn_type, CHANNEL)
    assert c is not None
    assert c.channel == CHANNEL
    assert c.open
    assert c.type == conn_type
    c.close()


def test_connection_sub():
    conn_type = Connection.Type.subscriber
    c = Connection('test', conn_type, CHANNEL)
    assert c is not None
    assert c.channel == CHANNEL
    assert c.open
    assert c.type == conn_type
    c.close()


def test_connection_req():
    conn_type = Connection.Type.requester
    c = Connection('test', conn_type, CHANNEL)
    assert c is not None
    assert c.channel == CHANNEL
    assert c.open
    assert c.type == conn_type
    c.close()


def test_connection_rep():
    conn_type = Connection.Type.replier
    c = Connection('test', conn_type, CHANNEL)
    assert c is not None
    assert c.channel == CHANNEL
    assert c.open
    assert c.type == conn_type
    c.close()


def test_connection_pusher():
    conn_type = Connection.Type.pusher
    c = Connection('test', conn_type, CHANNEL)
    assert c is not None
    assert c.channel == CHANNEL
    assert c.open
    assert c.type == conn_type
    c.close()


def test_connection_puller():
    conn_type = Connection.Type.puller
    c = Connection('test', conn_type, CHANNEL)
    assert c is not None
    assert c.channel == CHANNEL
    assert c.open
    assert c.type == conn_type
    c.close()

