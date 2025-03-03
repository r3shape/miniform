![logo](https://github.com/r3shape/r3engine/blob/main/r3engine/assets/r3-sticker.png?raw=true)  
![PyPi Package version](https://img.shields.io/pypi/v/r3frame?style=for-the-badge&logo=pypi&logoColor=white&label=r3frame&labelColor=black&color=white&link=https%3A%2F%2Fpypi.org%2Fproject%2Fr3frame%2F2025.0.2%2F
)  
![GitHub Stars](https://img.shields.io/github/stars/r3shape/r3frame?style=for-the-badge&label=stars&labelColor=black&color=white)
![License](https://img.shields.io/badge/mit-badge?style=for-the-badge&logo=mit&logoColor=white&label=License&labelColor=black&color=white)

## What is r3frame?  
**r3frame** is a game development framework designed to help developers create games with **more speed and less hassle**. It provides a structured foundation for handling scenes, objects, UI, input, and rendering, so you can focus on making games instead of reinventing the wheel.  

## Why Use r3frame?  
- **Save Time** – No need to build a game structure from scratch.  
- **Better Organization** – Scenes, assets, and objects are neatly managed.  
- **Pygame, but Better** – All the flexibility of Pygame, with added convenience.  

## Features  
- **Modularity** – Manage your game with a clean and modular API.  
- **Scene & Object Management** – Easily define and switch between game scenes.  
- **Custom UI System** – Buttons, text fields, and interface-scripting made simple.  
- **Asset Loading** – Load images and sprite sheets efficiently.  
- **Input Handling** – Keyboard and mouse events with built-in support.  
- **Partitioning Systems** – Efficient object management for game worlds of many sizes.  

## Installation  
Install **r3frame** via pip:  

```sh
pip install r3frame
```

## r3 Playground  
Once installed, you can run the **r3frame** playground demo by typing:  

```sh
r3playground
```

This will launch an interactive example that is actively maintained and used to showcase **r3frame**'s capabilities.  

## Quick Start
Getting started is as simple as the following code:
```python
import r3frame as r3

class MyGame(r3.app.Application):
    def __init__(self):
        super().__init__("My First r3frame Game")

    def load_scenes(self):
        self.set_scene(r3.app.scene.Scene("Main Scene", r3.objects.world.Grid_Map(50, 50, 32)))

    def load_assets(self):
        pass

    def load_objects(self):
        self.player = r3.objects.game.Game_Object(
            location=[100, 100], color=[0, 255, 0], size=[16, 16])

    def handle_events(self):
        if self.events.key_pressed(r3.app.inputs.Keyboard.Escape):
            self.events.quit = True
        if self.events.key_held(r3.app.inputs.Keyboard.A):
            self.player.set_velocity(vx=-self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.D):
            self.player.set_velocity(vx=self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.W):
            self.player.set_velocity(vy=-self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.S):
            self.player.set_velocity(vy=self.player.speed)

    def handle_update(self):
        self.player.update(self.clock.delta)
        self.camera.center_on(self.player.size, self.player.location)
    
    def handle_render(self):
        self.renderer.draw_call(self.player.image, self.player.location)

MyGame().run()
```

### Lets Take A Closer Look
r3frame is comprised of multiple sub-modules, all of which provide specific functionality and work together seamlessly.  
The first thing we do is *subclass* `r3frame.app.Application`. This object is responsible for the overall control-flow of your application. It handles calling update/render methods on all the *app-level* objects such as scenes, interfaces, and resources.  

The methods for loading scenes, assets, and objects are all required to be implemented and will raise a `NotImplementedError` if not found in an instance of `r3frame.app.Application`. The call order internally is (`load_scenes`, `load_assets` `load_objects`), as you first load and configure your game's scenes, then load in your assets, finally creating and configuring your objects in their respective scenes with their respective assets.

So with that in mind, we create ourselves a player object, and then setup some input handling to respond to some keyboard events. Now the application will handle *app-level* update and render calls, so its up to us to issue them for *game-level* operations. This happens to be fairly straightforward in this example as we update our player and center our camera, then issue a draw call for our player object.

With that we have a simple but easily extendible scene for us to create pretty much anything we'd dare imagine.  
Though, this world is a bit bland. Try adding some objects of varying colors and sizes to it!

## Contributing  
Want to help improve **r3frame**? Feel free to contribute by submitting issues, suggesting features, or making pull requests!  

## License  
**r3frame** is open-source under the **MIT License.**
