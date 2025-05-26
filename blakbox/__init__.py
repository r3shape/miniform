import blakbox.app as app
import blakbox.util as util

import blakbox.globs as globs
import blakbox.quotes as quotes
import blakbox.version as version
if "BLAKBOX_NO_PROMT" not in globs.os.environ:
    print(
        f'BLAKBOX {version.BLAKBOX_YEAR}.{version.BLAKBOX_MINOR}.{version.BLAKBOX_PATCH} | "{globs.random.choice(quotes.BLAKBOX_QUOTES)}"'
    )