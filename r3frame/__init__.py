import r3frame.app as app
import r3frame.app.ui as ui
import r3frame.game as game
import r3frame.util as util
import r3frame.version as version

from r3frame.globs import os
if "R3FRAME_NO_PROMT" not in os.environ:
    print(
        f"r3frame {version.R3FRAME_YEAR}.{version.R3FRAME_MINOR}.{version.R3FRAME_PATCH} | [ random quote here ]"
    )