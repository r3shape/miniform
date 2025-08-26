from miniform.imports import pg
import miniform

from .world.object import MiniStaticObject, MiniDynamicObject

class MiniCache(miniform.MiniAtom):
    def __init__(self, app):
        super().__init__()
        pg.font.init()
        pg.mixer.init()
        pg.display.init()
        self.app: miniform.app.MiniApp = app
        self.fonts = {}         # key -> (pg.Font, (path, size))
        self.sounds = {}        # key -> (pg.mixer.Sound, path)
        self.objects = {}       # key -> (MiniStaticObject|MiniDynamicObject)
        self.surfaces = {}      # key -> (pg.Surface, path)
        self.animations = {}    # key -> (list[pg.Surface], list[index, timer, duration, loop], path)

    def _serialize(self) -> dict:
        font_meta = []
        for key, font_data in self.fonts.items():
            path, size = font_data[1]
            font_meta.append([key, path, size])

        sound_meta = []
        for key, sound_data in self.sounds.items():
            path = sound_data[1]
            sound_data.append([key, path])

        object_meta = []
        for key, obj in self.objects.items():
            pos = obj.pos
            size = obj.size
            color = obj.color
            mass = getattr(obj, "mass", 0)
            static = obj.get_flag(miniform.MiniObjectFlag.OBJECT_STATIC)
            object_meta.append([key, pos, size, color, mass, static])

        surface_meta = []
        animation_meta = []

        return {
            "font-meta": font_meta,
            "sound-meta": sound_meta,
            "object-meta": object_meta,
            "surface-meta": surface_meta,
            "animation-meta": animation_meta
        }

    def configure(self, font_meta, sound_meta, object_meta, surface_meta, animation_meta) -> None:
        for key, path, size in font_meta:
            self.load_font(key, path, size)

        for key, path in sound_meta:
            self.load_sound(key, path)

        for key, pos, size, color, mass, static in object_meta:
            self.load_object(key, size, pos, mass, color, static)

    def _load_surface(self, path: str) -> pg.Surface:
        try:
            return pg.image.load(path).convert_alpha()
        except Exception as e:
            miniform.MiniLogger.error(f"[MiniCache] Failed to load surface '{path}': {e}")
            return None

    def _load_surface_array(self, path: str, frame_size: list[int]) -> list[pg.Surface]:
        sheet = self._load_surface(path)
        frame_x = sheet.get_width() // frame_size[0]
        frame_y = sheet.get_height() // frame_size[1]

        frames = []
        for row in range(frame_y):
            for col in range(frame_x):
                x = col * frame_size[0]
                y = row * frame_size[1]
                frame = pg.Surface(frame_size, pg.SRCALPHA).convert_alpha()
                frame.blit(sheet, [0, 0], pg.Rect([x, y], frame_size))  # texture sampling :)
                frames.append(frame)
        return frames

    def _load_font(self, path: str, size: int) -> pg.font.Font:
        try:
            return pg.font.Font(path, size)
        except Exception as e:
            miniform.MiniLogger.error(f"[MiniCache] Failed to load font '{path}' size {size}: {e}")
            return None

    def _load_sound(self, path: str) -> pg.mixer.Sound:
        try:
            return pg.mixer.Sound(path)
        except Exception as e:
            miniform.MiniLogger.error(f"[MiniCache] Failed to load sound '{path}': {e}")
            return None

    def load_surface(self, key: str, path: str) -> bool:
        if key in self.surfaces:
            miniform.MiniLogger.warning(f"[MiniCache] Surface already exists: '{key}'. Use reload_surface() to overwrite.")
            return False
        surface = self._load_surface(path)
        if surface:
            self.surfaces[key] = (surface, path)
            miniform.MiniLogger.info(f"[MiniCache] Surface loaded: (key){key} (path){path}")
            return True
        return False

    def reload_surface(self, key: str, path: str) -> bool:
        if key not in self.surfaces:
            miniform.MiniLogger.warning(f"[MiniCache] Surface not found: {key}")
            return False
        
        surface = self._load_surface(path)
        if surface:
            self.surfaces[key] = (surface, path)
            miniform.MiniLogger.info(f"[MiniCache] Reloaded surface with key: '{key}'")
            return True
        return False

    def get_surface(self, key: str) -> pg.Surface | None:
        return self.surfaces.get(key, (None,))[0]

    def unload_surface(self, key: str) -> None:
        if key not in self.surfaces:
            miniform.MiniLogger.warning(f"[MiniCache] Surface not found: {key}")
            return
        del self.surfaces[key]
        miniform.MiniLogger.info(f"[MiniCache] Unloaded surface with key: '{key}'")

    def load_animation(self, key: str, path: str, frame_size: list[int], frame_duration: float, loop: bool = True) -> None:
        if key in self.surfaces:
            miniform.MiniLogger.warning(f"[MiniCache] Animation already exists: '{key}'. Use reload_animation() to overwrite.")
            return False
        
        frames = self._load_surface_array(path, frame_size)
        if frames:
            self.animations[key] = [frames, [0, 0.0, len(frames), 1/frame_duration, loop], path]
            miniform.MiniLogger.info(f"[MiniCache] Animation loaded: (key){key} (path){path}")
            return True
        return False
    
    def reload_animation(self, key: str, path: str, frame_size: list[int], frame_duration: float, loop: bool = True) -> bool:
        if key not in self.animations:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: {key}")
            return False
        
        frames = self._load_surface_array(path, frame_size)
        if frames:
            self.animations[key] = [frames, [0, 0.0, len(frames), 1/frame_duration, loop]]
            miniform.MiniLogger.info(f"[MiniCache] Reloaded animation with key: '{key}'")
            return True
        return False

    def get_animation(self, key: str) -> list:
        return self.animations.get(key, None)

    def get_animation_frames(self, key: str) -> list:
        return self.animations.get(key, None)[0]

    def get_animation_data(self, key: str) -> list:
        return self.animations.get(key, None)[1]

    def get_animation_index(self, key: str) -> int:
        data = self.get_animation(key)
        if not data:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: '{key}'")
            return -1
        return data[1][0]

    def get_animation_timer(self, key: str) -> int:
        data = self.get_animation(key)
        if not data:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: '{key}'")
            return -1
        return data[1][1]

    def get_animation_duration(self, key: str) -> int:
        data = self.get_animation(key)
        if not data:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: '{key}'")
            return -1

        #frame duration
        return data[1][2]

        # total duration
        # return data[1][2] * len(data[0])

    def get_animation_frame(self, key: str) -> list:
        data = self.get_animation(key)
        if not data:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: '{key}'")
            return
        return data[0][data[1][0]]

    def reset_animation(self, key: str) -> None:
        data = self.get_animation(key)
        if not data:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: '{key}'")
            return
        data[1][1] = 0
        data[1][0] = 0

    def update_animation(self, key: str, dt: float) -> None:
        data = self.get_animation(key)
        if not data:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: '{key}'")
            return

        data[1][1] += dt
        if data[1][1] >= data[1][3]:
            data[1][1] = 0
            data[1][0] += 1
            if data[1][0] >= data[1][2]:
                if data[1][4]:
                    data[1][0] = 0
                else:
                    data[1][0] = data[1][2] - 1

    def unload_animation(self, key: str) -> None:
        if key not in self.animations:
            miniform.MiniLogger.warning(f"[MiniCache] Animation not found: {key}")
            return
        del self.animations[key]
        miniform.MiniLogger.info(f"[MiniCache] Unloaded animation with key: '{key}'")

    def load_font(self, key: str, path: str, size: int) -> bool:
        if key in self.fonts:
            miniform.MiniLogger.warning(f"[MiniCache] Font already exists: '{key}'. Use reload_font() to overwrite.")
            return False
        font = self._load_font(path, size)
        if font:
            self.fonts[key] = (font, (path, size))
            miniform.MiniLogger.info(f"[MiniCache] Font loaded: (key){key} (path){path}")
            return True
        return False

    def reload_font(self, key: str, path: str, size: int) -> bool:
        if key not in self.fonts:
            miniform.MiniLogger.warning(f"[MiniCache] Font not found: {key}")
            return False

        font = self._load_font(path, size)
        if font:
            self.fonts[key] = (font, (path, size))
            miniform.MiniLogger.info(f"[MiniCache] Reloaded font with key: '{key}'")
            return True
        return False

    def get_font(self, key: str) -> pg.font.Font | None:
        return self.fonts.get(key, (None,))[0]

    def unload_font(self, key: str) -> None:
        if key not in self.fonts:
            miniform.MiniLogger.warning(f"[MiniCache] Font not found: {key}")
            return
        del self.fonts[key]
        miniform.MiniLogger.info(f"[MiniCache] Unloaded font with key: '{key}'")

    def load_sound(self, key: str, path: str) -> bool:
        if key in self.sounds:
            miniform.MiniLogger.warning(f"[MiniCache] Sound already exists: '{key}'. Use reload_sound() to overwrite.")
            return False
        sound = self._load_sound(path)
        if sound:
            self.sounds[key] = (sound, path)
            miniform.MiniLogger.info(f"[MiniCache] Sound loaded: (key){key} (path){path}")
            return True
        return False

    def reload_sound(self, key: str, path: str) -> bool:
        if key not in self.sounds:
            miniform.MiniLogger.warning(f"[MiniCache] Sound not found: {key}")
            return False
        
        sound = self._load_sound(path)
        if sound:
            self.sounds[key] = (sound, path)
            miniform.MiniLogger.info(f"[MiniCache] Reloaded sound with key: '{key}'")
            return True
        return False

    def get_sound(self, key: str) -> pg.mixer.Sound | None:
        return self.sounds.get(key, (None,))[0]

    def unload_sound(self, key: str) -> None:
        if key not in self.sounds:
            miniform.MiniLogger.warning(f"[MiniCache] Sound not found: {key}")
            return
        del self.sounds[key]
        miniform.MiniLogger.info(f"[MiniCache] Unloaded sound with key: '{key}'")

    def load_object(
            self,
            key: str,
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            mass: float = 25.0,
            color: list[int] = [95, 205, 28],
            static: bool=True) -> MiniStaticObject|MiniDynamicObject|None:
            if not isinstance(self.app.world, miniform.resource.world.MiniWorld):
                miniform.MiniLogger.error(f"[MiniCache] World not set: '{key}'. A call to set_world() must be made first.")
                return None

            if key in self.objects:
                miniform.MiniLogger.warning(f"[MiniCache] Object already exists: '{key}'. Use reload_object() to overwrite.")
                return self.objects[key]
            
            if static:
                obj = miniform.resource.world.MiniStaticObject(
                    tag=key,
                    pos=pos,
                    size=size,
                    color=color,
                )
            else:
                obj = miniform.resource.world.MiniDynamicObject(
                    tag=key,
                    pos=pos,
                    size=size,
                    mass=mass,
                    color=color,
                )

            self.objects[key] = obj
            
            miniform.MiniLogger.info(f"[MiniCache] Object loaded: (key){key} (size){size} (pos){pos} (color){color}")
            return self.objects[key]

    def get_object(self, key: str) -> MiniStaticObject|MiniDynamicObject|None:
        return self.objects.get(key, None)

    def reload_object(
            self,
            key: str,
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            mass: float = 25.0,
            color: list[int] = [0, 0, 0],
            static: bool = True,
        ):
        if key not in self.objects:
            miniform.MiniLogger.warning(f"[MiniCache] Object not found: {key}")
            return None

        self.objects[key] = self.load_object(key, size, pos, mass, color, static)
        
        miniform.MiniLogger.info(f"[MiniCache] Reloaded object with key: '{key}'")
        return self.objects[key]
    
    def unload_object(self, key: str) -> None:
        if not isinstance(self.app.world, miniform.resource.world.MiniWorld):
                miniform.MiniLogger.error(f"[MiniCache] World not set: '{key}'. A call to set_world() must be made first.")
                return
        if key not in self.objects:
            miniform.MiniLogger.warning(f"[MiniCache] Object not found: {key}")
            return

        del self.objects[key]
        miniform.MiniLogger.info(f"[MiniCache] Unloaded object with key: '{key}'")

    def store_object(self, key: str, obj: MiniStaticObject|MiniDynamicObject) -> None:
        if key in self.objects:
            miniform.MiniLogger.warning(f"[MiniCache] Object already exists: '{key}'. Use reload_object() to overwrite.")
            return self.objects[key]

        self.objects[key] = obj
        self.app.world.add_object(self.objects[key])

        miniform.MiniLogger.info(f"[MiniCache] Stored object with key: '{key}'")

    def clear(self) -> None:
        self.fonts.clear()
        self.sounds.clear()
        self.objects.clear()
        self.surfaces.clear()
        self.animations.clear()
        miniform.MiniLogger.info("[MiniCache] Cleared all cached assets")
