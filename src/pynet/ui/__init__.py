from pynet import Logger

LOG = Logger('Pynet.UI', logger_to_console=True)

from .utils import *
from . import app
from . import vm
