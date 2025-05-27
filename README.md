<div align="center">

<img src="https://github.com/r3shape/BLAKBOX/blob/NIGHTBOX/blakbox/assets/images/logo-5x.gif?raw=true" alt="BLAKBOX Logo"/>  

<br><br>

![Version](https://img.shields.io/pypi/v/BLAKBOX?style=for-the-badge&logo=pypi&logoColor=white&label=BLAKBOX&labelColor=black&color=white&link=https%3A%2F%2Fpypi.org%2Fproject%2FBLAKBOX%2F2025.0.2%2F) 
![Version](https://img.shields.io/pypi/v/NIGHTBOX?style=for-the-badge&logo=pypi&logoColor=white&label=NIGHTBOX&labelColor=black&color=white&link=https%3A%2F%2Fpypi.org%2Fproject%2FNIGHTBOX%2F2025.0.2%2F)  
![GitHub Stars](https://img.shields.io/github/stars/r3shape/BLAKBOX?style=for-the-badge&label=stars&labelColor=black&color=white)
![License](https://img.shields.io/badge/mit-badge?style=for-the-badge&logo=mit&logoColor=white&label=License&labelColor=black&color=white)  
![Build](https://github.com/r3shape/BLAKBOX/actions/workflows/NIGHTBOX.yml/badge.svg)  
![Build](https://github.com/r3shape/BLAKBOX/actions/workflows/BLAKBOX.yml/badge.svg)  

</div>

---

# BLAKBOX

## What?
**BLAKBOX** is a game development framework designed to help developers **create more with less hassle**. It provides a structured foundation for handling scenes, objects, UI, input, and rendering, so you can focus on making games instead of reinventing the wheel.

## Why?
- **Save Time** – No need to build a game structure from scratch.
- **Better Organization** – Scenes, assets, and objects are neatly managed.
- **Pygame, but Better** – All the flexibility of Pygame, with added convenience.

## Content?
- **Modularity** – Manage your game with a clean and modular API.
- **Scene & Object Management** – Easily define and switch between game scenes.
- **Custom UI System** – Buttons, text fields, and interface-scripting made simple.
- **Asset Loading** – Load images and sprite sheets efficiently.
- **Input Handling** – Keyboard and mouse events with built-in support.
- **Partitioning Systems** – Efficient object management for game worlds of many sizes.

## Download?
Install **BLAKBOX** via pip:

```sh
pip install BLAKBOX
```

## Getting Started?
After youv'e installed `blakbox` go ahead and create a script named `main.py` somwhere and paste in this code:

```python
import blakbox

class MyGame(blakbox.app.BOXapplication):
    def __init__(self) -> None:
        super().__init__(
            name = "My Game",           # initial window title
            window_size = [800, 600],   # the window itself
            display_size = [1600, 1200] # the surface "within" the window 
        )

    def configure(self): pass
    def cleanup(self): pass
    def handle_events(self): pass
    def handle_update(self): pass

if __name__ == "__main__":
    MyGame().run()
```
| NOTE: The methods `configure()`, `cleanup()`, `handle_events()` and `handle_update()` must be defined for any instance of `BOXapplication`.

Above is the minimal code needed to get `BOXapplication` up and running. From here you can explore the `BOXscene` and the other classes provided in `blakbox.app.resource` and `blakbox.app.ui`.

Check out the `blakbox/examples` directory to get a look at some "real world" use cases for the library, maybe even kickstart your next project.

## Contributions?  
Want to help improve **BLAKBOX**? Feel free to contribute by submitting issues, suggesting features, or making pull requests!  

## License  
**BLAKBOX** is open-source under the **MIT License.**
</div>
