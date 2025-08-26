# miniform - A neat little thing...
from miniform.globals import *

from miniform.atom import MiniAtom
from miniform.log import MiniLogger

import miniform.utils as utils

import miniform.core.app as app
import miniform.core.process as process
import miniform.core.resource as resource

import os, random
if "MINIFORM_NO_PROMT" not in os.environ:
    from .quotes import MiniQuotes
    from .version import MINI_MAJOR, MINI_MINOR, MINI_PATCH
    print(
        f'Miniform {MINI_MAJOR}.{MINI_MINOR}.{MINI_PATCH} | "{random.choice(MiniQuotes)}"'
    )