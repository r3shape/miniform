from blakbox.globs import os, re, pg
# from blakbox.app.resource.audio import BOXaudio
from blakbox.app.resource.surface import BOXsurface
from blakbox.app.resource.surfarray import BOXsurfarray
from blakbox.app.resource.surfatlas import BOXsurfatlas

from blakbox.app.resource.object import BOXobject, OBJECT_FLAG

# ------------------------------------------------------------ #
class BOXresources:
    def __init__(self, atlas_size: list[int]) -> None:
        self.fonts: dict = {}
        self.sounds: dict = {}
        self.objects: dict[str, BOXobject] = {}
        self.surfaces: dict[str, BOXsurface] = {}
        self.surfarrays: dict[str, BOXsurfarray] = {}
        self.atlas: BOXsurfatlas = BOXsurfatlas(atlas_size)
   
    def pg_load_surface(self, path: str, scale: list[int] = None, color_key: list[int] = None) -> pg.Surface:
        surface = pg.image.load(path).convert_alpha()
        if color_key:
            surface.set_colorkey(color_key)
        if scale:
            surface = self.scale_surface(surface, scale)
        return surface

    def pg_surface_visible(self, surface: pg.Surface, threshold: int = 1) -> bool:
        pixels, transparent = 0, 0
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x, y)).a == 0:
                    transparent += 1
                pixels += 1
        return (pixels - transparent) >= threshold

    def pg_load_surface_sheet(self, path: str, frame_size: list[int], scale: list[int] = None, color_key: list[int] = None) -> list[pg.Surface]:
        sheet: pg.Surface = pg.image.load(path)
        
        frames = []
        frame_x = sheet.get_width() // frame_size[0]
        frame_y = sheet.get_height() // frame_size[1]

        for row in range(frame_y):
            for col in range(frame_x):
                x = col * frame_size[0]
                y = row * frame_size[1]
                frame = pg.Surface(frame_size, pg.SRCALPHA).convert_alpha()
                if color_key:
                    frame.set_colorkey(color_key)
                frame.blit(sheet, (0, 0), pg.Rect((x, y), frame_size))
                if scale:
                    frame = self.scale_surface(frame, scale)
                frames.append(frame)
        return frames

    def load_font(self, tag: str) -> None: pass
    def load_audio(self, tag: str) -> None: pass

    def apply_surface(self, object_tag: str, surface_tag: str) -> None:
        o = self.get_object(object_tag)
        s = self.get_surface(surface_tag)
        if o is None or s is None: return
        o.atlas_id = s.id
        o.atlas_tag = s.atlas_tag
        self.atlas.blit(s.id, o.surface, pos=[0, 0], data=s.data)

    def apply_surfarray(self, object_tag: str, surfarray_tag: str) -> None:
        o = self.get_object(object_tag)
        s = self.get_surfarray(surfarray_tag)
        if o is None or s is None: return
        o.atlas_id = s.id
        o.atlas_tag = s.atlas_tag
        self.atlas.blit(s.id, o.surface, pos=[0, 0], data=s.data)

    def get_object(self, tag: str) -> BOXobject:
        return self.objects.get(tag, None)
    
    def get_surface(self, tag: str) -> BOXsurface:
        return self.surfaces.get(tag, None)

    def get_surfarray(self, tag: str) -> BOXsurfarray:
        return self.surfarrays.get(tag, None)

    def rem_object(self, tag: str) -> BOXobject:
        rem = self.objects.pop(tag, None)
        print(f"Removed Object: (tag){tag} {rem}")
        return rem

    def rem_surface(self, tag: str) -> BOXsurface:
        rem = self.surfaces.pop(tag)
        print(f"Removed Surface: (tag){tag} {rem}")
        return rem

    def rem_surfarray(self, tag: str) -> BOXsurfarray:
        rem = self.surfarrays.pop(tag)
        print(f"Removed Surfarray: (tag){tag} {rem}")
        return rem

    def store_object(self, tag: str, object: BOXobject) -> None:
        if not isinstance(object, BOXobject): return
        if self.get_object(tag) is not None: return
        self.objects[tag] = object
        print(f"Stored Object: (tag){tag}: {self.objects[tag]}")

    def store_surface(self, tag: str, surface: BOXsurface) -> None:
        if not isinstance(surface, BOXsurface): return
        if self.get_surface(tag) is not None: return
        self.surfaces[tag] = surface
        print(f"Stored Surface: (tag){tag}: {self.surfaces[tag]}")

    def store_surfarray(self, tag: str, surfarray: BOXsurfarray) -> None:
        if not isinstance(surfarray, BOXsurfarray): return
        if self.get_surfarray(tag) is not None: return
        self.surfarrays[tag] = surfarray
        print(f"Stored Surfarray: (tag){tag}: {self.surfarrays[tag]}")

    def load_object(
            self,
            tag: str,
            size: list[int],
            pos: list[float] = [0, 0],
            bounds: list[int] = [0, 0],
            color: list[int] = [0, 0, 0],
        ) -> None:
        if self.objects.get(tag, False) != False: return
        self.objects[tag] = BOXobject(tag, size[:], pos[:], bounds[:], color[:])
        print(f"Loaded Object: (tag){tag} {self.objects[tag]}")

    def load_surface(self, tag: str, size: list[int], path: str) -> None:
        if self.surfaces.get(tag, False) != False: return
        self.surfaces[tag] = BOXsurface(self.atlas.load_surface(size, path, [1, 1]), tag, path, size)
        print(f"Loaded Surface: (tag){tag} {self.surfaces[tag]}")

    def load_surfarray(self, tag: str, size: list[int], layout: list[int], path: str, loop: bool = True, speed: float = 5.0) -> None:
        if self.surfarrays.get(tag, False) != False: return
        self.surfarrays[tag] = BOXsurfarray(self.atlas.load_surface(size, path, layout), tag, path, size, layout, loop, speed)
        print(f"Loaded Surfarray: (tag){tag} {self.surfarrays[tag]}")
# ------------------------------------------------------------ #
