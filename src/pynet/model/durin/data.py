from dataclassy import dataclass
from .. import Url
from .. import DDict

URLS = DDict(
    server=DDict(
        demander=Url.Remote(ip='*', port=28128),
        console=Url.Remote(ip='*', port=28129),
    ),
    client=DDict(
        demander=Url.Remote(port=28128),
        console=Url.Remote(port=28129),
    )
)


@dataclass(unsafe_hash=True, slots=True, init=True, repr=True)
class Execute:
    command: str = ''
