from pynet.model import Size


def test_size():
    assert Size.obj_size(int()) == 24
