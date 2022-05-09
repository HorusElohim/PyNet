from dataclassy import dataclass
from .. import Url

URL_CONSOLE_SERVER = Url.Remote(ip='*', port=28128)
URL_CONSOLE_CLIENT = Url.Remote(port=28128)
URL_REQUEST_SERVER = Url.Remote(ip='*', port=28129)
URL_REQUEST_CLIENT = Url.Remote(port=28129)


@dataclass(unsafe_hash=True, slots=True, init=True)
class Execute:
    command: str = ''


@dataclass(unsafe_hash=True)
class Exit:
    pass
