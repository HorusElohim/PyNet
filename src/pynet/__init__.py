__version__ = '2.0.1'
from os import mkdir
from pathlib import Path

RUN_FOLDER = '.run'
LOG_FOLDER = 'logs'
RUN_PATH = Path().cwd() / RUN_FOLDER
LOG_PATH = Path().cwd() / LOG_FOLDER

if not RUN_PATH.exists():
    mkdir(RUN_PATH)

if not LOG_PATH.exists():
    mkdir(LOG_PATH)

from . import model
from . import console
