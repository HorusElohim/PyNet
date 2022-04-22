from pynet.model import profile


@profile
def profile_function():
    s = 0
    for x in range(0, 1000):
        s += x
    return s


def test_size():
    assert profile_function() == 499500
