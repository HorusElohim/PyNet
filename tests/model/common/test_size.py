from pynet.model.common import Size


def test_size():
    assert Size.obj_size(int()) == 24
