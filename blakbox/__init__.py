import blakbox.app as app
import blakbox.game as game
import blakbox.util as util
from blakbox.atom import Atom
import blakbox.version as version
import blakbox.quotes as quotes

from blakbox.globs import os, random
if "BLAKBOX_NO_PROMT" not in os.environ:
    print(
        f'BLAKBOX {version.BLAKBOX_YEAR}.{version.BLAKBOX_MINOR}.{version.BLAKBOX_PATCH} | "{random.choice(quotes.BLAKBOX_QUOTES)}"'
    )