from r3frame.globs import pg
from r3frame.app.camera import Camera
from r3frame.app.resource.image import Image

# ------------------------------------------------------------ #
class Renderer:
    """
    Handles rendering of objects to the display, with support for different rendering strategies 
    optimized for small and large game worlds.
    """
    
    class FLAGS:
        SHOW_CAMERA: int = 1 << 0  # flag to display the camera's viewport boundaries.

    def __init__(self, camera: Camera) -> None:
        """
        Initializes the renderer with a target window and camera.

        :param window: The game window where rendering occurs.
        :param camera: The camera that defines the viewport.
        """
        self.camera = camera
        self.window = camera.window
        self.target = self.window.display
        self.flags = 0
        self.draw_calls = 0
        self._draw_calls = []  # draw_call layout : [image, location]

    def set_flag(self, flag: int) -> None:
        """Enables a rendering flag."""
        self.flags |= flag

    def rem_flag(self, flag: int) -> None:
        """Disables a rendering flag."""
        if (self.flags & flag) == flag:
            self.flags &= ~flag

    def pre_render(self) -> None: pass
    
    def post_render(self) -> None: pass

    def draw_call(self, image: Image, location: list[int]) -> None:
        """
        Queues a draw call for rendering.

        :param surface: The image/surface to render.
        :param location: The world-space position of the surface.
        
        Performs frustum culling to avoid rendering objects outside of the viewport.
        """
        if self.draw_calls + 1 > 4096:  # prevent excessive draw calls.
            return

        # frustum culling
        if ((location[0] + image.size[0]) - self.window.clip_range[0] < self.camera.location[0] or 
            location[0] + self.window.clip_range[0] > self.camera.location[0] + self.camera.viewport_size[0]) or \
           ((location[1] + image.size[1]) - self.window.clip_range[1] < self.camera.location[1] or 
            location[1] + self.window.clip_range[1] > self.camera.location[1] + self.camera.viewport_size[1]):
            return

        self._draw_calls.append([image, location])
        self.draw_calls += 1

    def render(self) -> None:
        """
        Renders objects to a viewport-sized surface before scaling it up to the display.
        
        Solves the **display transformation bottleneck** by limiting rendering to objects within 
        the camera's viewport, making it efficient for **large game worlds**. Since transformations 
        are applied at the render-target/display level, object positions remain true to world coordinates.
        """
        del self.target
        self.target = pg.Surface(self.camera.viewport_size)  # create a surface matching the viewport size.
        self.target.fill(self.window.color)
        self.window.clear()

        self.pre_render()
        for i in range(self.draw_calls):
            image, location = self._draw_calls.pop(0)
            self.window.blit(image, location)
        self.draw_calls = 0
        self.post_render()

        if (self.flags & self.FLAGS.SHOW_CAMERA):
            self.window.blit_rect(self.camera.get_viewport(), [255, 255, 255], 1)
            self.window.blit_rect(self.camera.get_center([10, 10]), [0, 255, 0], 1)
        
        # apply camera transformations at the render-target level (no per-object transformations)
        self.target.blit(self.window.display, [-self.camera.location[0], -self.camera.location[1]])
        self.window.window.blit(
            pg.transform.scale(self.target, self.window.size),
            [0, 0]
        )
# ------------------------------------------------------------ #
