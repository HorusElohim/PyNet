from pynet.model.network import Manipulator

DATA = [1, 2, 3, 4, 6, 8, 9]


def test_manipulator():
    data_com = Manipulator.compress(Manipulator.encode(DATA))
    data_dec = Manipulator.decode(Manipulator.decompress(data_com))
    assert DATA == data_dec
