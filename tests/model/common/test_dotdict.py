from pynet.model.common.ddict import DDict


def test_dotdict():
    dd = DDict(test=1)
    assert dd.test == 1
    dd.new = 2
    assert dd.new == 2
