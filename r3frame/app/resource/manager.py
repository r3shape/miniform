from r3frame.globs import os, re, pg
from r3frame.app.resource.base import Resource
# from r3frame.app.resource.sound import Sound
from r3frame.app.resource.image import Image
from r3frame.app.resource.animation import Animation

# ------------------------------------------------------------ #
class ResourceManager:
    def __init__(self) -> None:
        self.font:dict = {}
        self.sound:dict = {}
        self.image:dict[str, Image] = {}
        self.animation:dict[str, Animation] = {}

        self.create_surface = lambda size, color: pg.Surface(size)
        self.create_rect = lambda location, size: pg.Rect(location, size)

        self.fill_surface = lambda surface, color: surface.fill(color)
        self.flip_surface = lambda surface, x, y: pg.transform.flip(surface, x, y)
        self.scale_surface = lambda surface, scale: pg.transform.scale(surface, scale)
        self.rotate_surface = lambda surface, angle: pg.transform.rotate(surface, angle)

    def flip_image(self, key: str, x: bool, y: bool) -> None:
        try:
            image = self.image[key]
            if isinstance(image, pg.Surface):
                self.image[key] = self.flip_surface(image, x, y)
            elif isinstance(image, list):
                self.image[key] = [self.flip_surface(i, x, y) for i in image]
        except (KeyError) as err: print(err)

    def get_image(self, key:str) -> Image|None:
        return self.image.get(key, None)
    
    def set_image(self, key:str, image:pg.Surface) -> None:
        try:
            self.image[key].data = image
        except (KeyError) as err: print(err)

    def load_image(self, key:str, path:str, scale:list=None, colorKey:list=None) -> Image:
        try:
            image:pg.Surface = pg.image.load(path).convert_alpha()
            image.set_colorkey(colorKey)
            if scale: image = self.scale_surface(image, scale)
            
            rid = len(self.image.values())
            self.image[key] = Image(rid, image)
            return self.image[key]
        except (FileNotFoundError) as err: print(err)
    
    def load_animation(
            self,
            key: str, sheet_path: str,
            frame_size: list[int], scale: list=None, colorKey: list=None,
            loop: bool=True, frame_duration: int= 5, frame_offset: list[int]=[0, 0]
        ) -> Animation:
        try:
            frames = self.load_image_sheet(key, sheet_path, frame_size, scale, colorKey)
            rid = len(self.animation.values())
            self.animation[key] = Animation(rid, frames, loop, frame_duration, frame_offset)
            return self.animation[key]
        except FileNotFoundError as e: return None

    def load_image_dir(self, key:str, path:str, scale:list=None, colorKey:list=None) -> list:
        try:
            rid = len(self.image.values())
            images:list[Image] = []
            for _, __, image in os.walk(path):
                sorted_images = sorted(image, key=lambda string_: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)])
                for image in sorted_images:
                    full_path = path + '/' + image
                    image_surface = self.load_image(full_path, scale, colorKey)
                    if self.image_visible(image_surface):
                        img = Image(rid, image_surface)
                        images.append(img)
                        rid += 1
            self.image[key] = images
            return self.image[key]
        except (FileNotFoundError) as err: ...
    
    def load_image_sheet(self, key: str, path: str, frame_size: list[int], scale: list=None, colorKey: list=None) -> list:
        try:
            sheet: Image = self.load_image(key, path)
            frame_x = int(sheet.size[0] / frame_size[0])
            frame_y = int(sheet.size[1] / frame_size[1])
            
            rid = len(self.image.values())
            frames: list[Image] = []
            for row in range(frame_y):
                for col in range(frame_x):
                    x = col * frame_size[0]
                    y = row * frame_size[1]
                    frame = Image(rid, pg.Surface(frame_size, pg.SRCALPHA).convert_alpha())
                    frame.data.set_colorkey(colorKey)
                    frame.data.blit(sheet.data, (0,0), pg.Rect((x, y), frame_size))   # blit the sheet at the desired coords (texture mapping)
                    if scale: frame.data = self.scale_surface(frame, scale)
                    if self.image_visible(frame):
                        frames.append(frame)
                        rid += 1
            self.image[key] = frames
            return self.image[key]
        except FileNotFoundError as e: return None

    def image_visible(self, image: Image, threshold: int=1) -> bool:
        result = False
        pixels, noPixels = 0, 0
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                pixel = image.data.get_at([x, y])
                if pixel[3] == 0:
                    noPixels += 1
                pixels += 1
        if pixels-noPixels >= threshold:
            result = True
        return result
# ------------------------------------------------------------ #
