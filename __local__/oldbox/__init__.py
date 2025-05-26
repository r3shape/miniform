import oldbox.app as app
import oldbox.game as game
import oldbox.util as util
from oldbox.atom import Atom
import oldbox.version as version
import oldbox.quotes as quotes

from oldbox.globs import os, random
if "BLAKBOX_NO_PROMT" not in os.environ:
    print(
        f'BLAKBOX {version.BLAKBOX_YEAR}.{version.BLAKBOX_MINOR}.{version.BLAKBOX_PATCH} | "{random.choice(quotes.BLAKBOX_QUOTES)}"'
    )