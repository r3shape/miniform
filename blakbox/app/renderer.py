from blakbox.globs import pg
from blakbox.util import scale_v2
from blakbox.atom import Atom
from blakbox.app.window import Window
from blakbox.app.camera import Camera
from blakbox.game.resource import Image, Animation
from blakbox.game.resource.surfmap import SurfMap

# ------------------------------------------------------------ #
class Renderer(Atom):
    class FLAGS:
        SHOW_CAMERA: int = 1 << 0  # flag to display the camera's viewport boundaries.

    def __init__(self, surfmap: SurfMap, camera: Camera) -> None:
        super().__init__(0, 0)
        self.draw_calls = 0
        self._draw_calls = []
        self.camera: Camera = camera
        self.surfmap: SurfMap = surfmap
        self.window: Window = camera.window

    def pre_render(self) -> None:   pass
    def post_render(self) -> None:  pass

    def draw_call(self, image: Image|Animation, pos: list[int]) -> None:
        """
        Queues a draw call for rendering.

        :param surface: The image/surface to render.
        :param pos: The world-space position of the surface.
        
        Performs frustum culling to avoid rendering objects outside of the viewport.
        """
        if self.draw_calls + 1 > 4096:  # prevent excessive draw calls.
            return

        # frustum culling
        if ((pos[0] + image.size[0]) - self.window.clip_range[0] < self.camera.pos[0] or 
             pos[0] + self.window.clip_range[0] > self.camera.pos[0] + self.camera.bounds[0]) or \
           ((pos[1] + image.size[1]) - self.window.clip_range[1] < self.camera.pos[1] or 
             pos[1] + self.window.clip_range[1] > self.camera.pos[1] + self.camera.bounds[1]):
            return
        
        self._draw_calls.append([pos[1], image, pos])
        self.draw_calls += 1

    def render(self) -> None:
        self.target = pg.Surface(self.camera.viewport_size)  # create a surface matching the viewport size.
        self.target.fill(self.window.clear_color)
        self.window.fill()

        self.pre_render()
        self._draw_calls.sort(key=lambda call: call.pop(0))
        for i in range(self.draw_calls):
            image, pos = self._draw_calls.pop(0)
            if isinstance(image, Image) or isinstance(image, Animation):
                self.surfmap.blit(image.id, self.window.display, pos, frame_data=image.frame_data)
            else:
                self.window.blit(image, pos)
        self.draw_calls = 0
        self.post_render()

        if self.get_state(self.FLAGS.SHOW_CAMERA):
            self.window.blitr(self.camera.viewport_rect, color=[255, 255, 255], width=1)
            self.window.blitr(self.camera.center_rect([10, 10]), color=[0, 255, 0], width=1)
        
        # apply camera transformations at the render-target level (no per-object transformations)
        self.target.blit(self.window.display, self.camera.offset)
        self.window.screen.blit(dest=[0, 0], source=pg.transform.scale(self.target, self.window.screen_size))
# ------------------------------------------------------------ #
