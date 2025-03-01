from r3frame.globals import pg

class Event_Manager:
    quit: bool=False

    keyboard = {}
    mouse_old = {}
    keyboard_old = {}
    mouse = {
        1:False,
        2:False,
        3:False,
        4:False,
        5:False,
        6:False,
        7:False
    }
    mouse_location = (0,0)
    mouse_wheel_up: bool=False
    mouse_wheel_down: bool=False

    @classmethod
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

    @classmethod
    def key_held(self, key):
        return self.keyboard.get(key, False)

    @classmethod
    def key_pressed(self, key):
        return self.keyboard.get(key, False) and not self.keyboard_old.get(key, False)
    
    @classmethod
    def mouse_held(self, button:int):
        return self.mouse.get(button, False)

    @classmethod
    def mouse_pressed(self, button):
        return self.mouse.get(button, False) and not self.mouse_old.get(button, False)
    