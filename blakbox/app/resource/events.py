from blakbox.globs import pg

# ------------------------------------------------------------ #
class BOXevents:
    def __init__(self) -> None:
        self.quit: bool=False

        self.mouse = {}
        self.keyboard = {}
        self.mouse_old = {}
        self.keyboard_old = {}
        self.mouse = {
            1:False,
            2:False,
            3:False,
            4:False,
            5:False,
            6:False,
            7:False
        }
        self.mouse_location = (0,0)
        self.mouse_wheel_up: bool=False
        self.mouse_wheel_down: bool=False

    def update(self) -> int:
        self.mouse_wheel_up = False
        self.mouse_wheel_down = False
        self.mouse_old = self.mouse.copy()
        self.keyboard_old = self.keyboard.copy()
        self.mouse_location = pg.mouse.get_pos()
        
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_F12):
                self.quit = True
            match event.type:
                case pg.KEYUP:
                    self.keyboard[event.key] = False
                case pg.KEYDOWN:
                    self.keyboard[event.key] = True
                case pg.MOUSEBUTTONUP:
                    self.mouse[event.button] = False
                case pg.MOUSEBUTTONDOWN:
                    self.mouse[event.button] = True
                    if event.button == 4:
                        self.mouse_wheel_up = True
                    if event.button == 5:
                        self.mouse_wheel_down = True

    def key_held(self, key):
        return self.keyboard.get(key, False)

    def key_pressed(self, key):
        return self.keyboard.get(key, False) and not self.keyboard_old.get(key, False)
    
    def mouse_held(self, button:int):
        return self.mouse.get(button, False)

    def mouse_pressed(self, button):
        return self.mouse.get(button, False) and not self.mouse_old.get(button, False)
# ------------------------------------------------------------ #
