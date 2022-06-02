from pynet.model.common import profile


@profile
def profile_function():
    return True


def test_size():
    assert profile_function()
