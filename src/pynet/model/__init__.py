from typing import Any, Dict


def kwargs_control(var: Any, kwargs: Dict[str, Any]) -> Any:
    var_name = next(iter(locals()))
    if var_name in kwargs:
        return kwargs[var_name]
    else:
        return var


from .common import *
from .abc import AbcEntity

PYNET_LOGGER = Logger('PyNet')

from .data import *
from .network import *
