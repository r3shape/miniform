import blakbox.app as app
import blakbox.utils as utils

import blakbox.globals as globals
import blakbox.quotes as quotes
import blakbox.version as version
if "BLAKBOX_NO_PROMT" not in globals.os.environ:
    print(
        f'BLAKBOX {version.BLAKBOX_YEAR}.{version.BLAKBOX_MINOR}.{version.BLAKBOX_PATCH} | "{globals.random.choice(quotes.BLAKBOX_QUOTES)}"'
    )