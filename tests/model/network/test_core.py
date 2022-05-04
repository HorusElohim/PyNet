from pynet.model.network.core import Core, CoreType
from pynet.model.network.url import Url
import pytest


# _______ Core Section _______

@pytest.mark.parametrize(
    'core_type',
    [CoreType.publisher,
     CoreType.subscriber,
     CoreType.pusher,
     CoreType.puller,
     CoreType.replier,
     CoreType.requester,
     ])
def test_core_local(core_type):
    core = Core('TestCore', core_type, Url.Local())
    assert core.core_type == core_type
    assert not core.is_open()
    core.open()
    assert core.is_open()
    core.close()
    assert not core.is_open()


@pytest.mark.parametrize(
    'core_type',
    [CoreType.publisher,
     CoreType.subscriber,
     CoreType.pusher,
     CoreType.puller,
     CoreType.replier,
     CoreType.requester,
     ])
def test_core_remote(core_type):
    core = Core('TestCore', core_type, Url.Remote())
    assert core.core_type == core_type
    assert not core.is_open()
    core.open()
    assert core.is_open()
    core.close()
    assert not core.is_open()
