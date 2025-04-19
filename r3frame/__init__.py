from r3frame.proc import Process
from r3frame.event import EventManager
from r3frame.input import Keyboard, Mouse
from r3frame.rsrc import Clock, Window, Camera, Renderer, AssetManager, Tilemap
from r3frame.util import sine_wave_value, damp_exp, damp_lin, point_inside, dist_to, angle_to

import r3frame.ui as ui
import r3frame.game as game
import r3frame.version as version

from r3frame.globs import os
if "R3FRAME_NO_PROMT" not in os.environ:
    print(
        f"r3frame {version.R3FRAME_YEAR}.{version.R3FRAME_MINOR}.{version.R3FRAME_PATCH} | [ random quote here ]"
    )