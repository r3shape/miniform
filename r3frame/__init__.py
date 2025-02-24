import r3frame.utils as utils
import r3frame.application as app
import r3frame.objects as objects
import r3frame.version as version

from r3frame.globals import os
if "R3FRAME_NO_PROMT" not in os.environ:
    print(
        f"r3frame {version.R3FRAME_YEAR}.{version.R3FRAME_MINOR}.{version.R3FRAME_PATCH} | [ random quote here ]"
    )