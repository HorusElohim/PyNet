from dataclassy import dataclass
from .. import SockUrl
from .. import DDict

URLS = DDict(
    server=DDict(
        demander=SockUrl.Remote(SockUrl.SERVER, ip='*', port=28128),
        console=SockUrl.Remote(SockUrl.SERVER, ip='*', port=28129),
    ),
    client=DDict(
        demander=SockUrl.Remote(SockUrl.CLIENT, port=28128),
        console=SockUrl.Remote(SockUrl.CLIENT, port=28129),
    )
)


@dataclass(unsafe_hash=True, slots=True, init=True, repr=True)
class Execute:
    command: str = ''
