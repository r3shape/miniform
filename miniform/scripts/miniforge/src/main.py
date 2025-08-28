from .globals import miniform, json
from .editor import MiniEditor
from .version import MF_MAJOR, MF_MINOR, MF_PATCH

class Miniforge(miniform.app.MiniApp):
    def __init__(self) -> None:
        super().__init__()
        if self._load_settings():
            super().__init__(
                title=f"MiniForge {MF_MAJOR}.{MF_MINOR}.{MF_PATCH}",
                window_size=self.settings["app"]["ws"],
                window_color=self.theme["clear-color"]
            )
        else: self.exit()

    @miniform.MiniProfile
    def _load_settings(self) -> bool:
        self.theme: dict = None
        self.settings: dict = None
        with open(miniform.utils._miniform_path("scripts/miniforge/external/.data/settings.json"), "r") as settings:
            try:
                # load settings
                self.settings = json.load(settings)
            
                # load binds
                self.mouse_binds: dict[str, int] = {k: getattr(self.mouse, v, None) for k, v in self.settings["app"]["binds"]["mouse"].items()}
                self.key_binds: dict[str, int] = {k: getattr(self.keyboard, v, None) for k, v in self.settings["app"]["binds"]["keyboard"].items()}

                # load theme
                with open(miniform.utils._miniform_path(f"scripts/miniforge/external/.data/themes/{self.settings['app']['theme']}.json"), "r") as theme:
                    self.theme = json.load(theme)
            except json.JSONDecodeError as e:
                miniform.MiniLogger.error("[Miniforge] failed to load app settings...")
                return False
        miniform.MiniLogger.debug("[Miniforge] the forge brightens...")
        return True

    @miniform.MiniProfile
    def init(self) -> None:
        self.cache.load_font("slkscr", miniform.utils._miniform_path("scripts/miniforge/external/.data/assets/fonts/slkscr.ttf"), 18)
        self.cache.load_surface("logo", miniform.utils._miniform_path("scripts/miniforge/external/.data/assets/images/wf3/Logo.ico"))
        
        self.cache.load_surface("draw", miniform.utils._miniform_path("scripts/miniforge/external/.data/assets/images/icon/Draw.png"))
        self.cache.load_surface("fill", miniform.utils._miniform_path("scripts/miniforge/external/.data/assets/images/icon/Fill.png"))
        self.cache.load_surface("eraser", miniform.utils._miniform_path("scripts/miniforge/external/.data/assets/images/icon/Eraser.png"))
        
        self.cache.load_animation("load-anim", miniform.utils._miniform_path("scripts/miniforge/external/.data/assets/images/icon/Loading.png"), [16, 16], 11)
        self.window.set_icon(self.cache.get_surface("logo"))
        
        self.set_world(MiniEditor)

    def exit(self) -> None:
        miniform.MiniLogger.debug("[Miniforge] the forge darkens...")

def main() -> None:
    Miniforge().run()

if __name__ == '__main__':
    main()
