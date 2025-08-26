<div align="center">
<img src="miniform/assets/images/icon.png" alt="miniform Logo"/>  

<h3>Miniform</h3>

![Version](https://img.shields.io/pypi/v/miniform?style=for-the-badge&logo=pypi&logoColor=white&label=miniform&labelColor=black&color=white&link=https%3A%2F%2Fpypi.org%2Fproject%2Fminiform%2F2025.0.2%2F)  
![GitHub Stars](https://img.shields.io/github/stars/r3shape/miniform?style=for-the-badge&label=stars&labelColor=black&color=white)
![License](https://img.shields.io/badge/mit-badge?style=for-the-badge&logo=mit&logoColor=white&label=License&labelColor=black&color=white)  
![Build](https://github.com/r3shape/miniform/actions/workflows/miniform.yml/badge.svg)  

</div>

## What?
**miniform** is a game development framework designed to help developers **create more with less hassle**. It provides a structured foundation for handling Worlds, objects, UI, input, and rendering, so you can focus on making games instead of reinventing the wheel.

## Why?
- **Save Time** – No need to build a game structure from scratch.
- **Better Organization** – Worlds, assets, and objects are neatly managed.
- **Pygame, but Better** – All the flexibility of Pygame, with added convenience.

## Content?
- **Modularity** – Manage your game with a clean and modular API.
- **World & Object Management** – Easily define and swap worlds.
- **Custom UI System** – Interface-scripting made simple.
- **Asset Loading** – Load sprites and animations efficiently.
- **Input Handling** – Keyboard and mouse events with built-in support.
- **Partitioning Systems** – Efficient object management for game worlds of any size.

## Download?
Install **miniform** via pip:

```sh
pip install miniform
```

## Getting Started?
After youv'e installed `miniform` go ahead and create a script named `main.py` somwhere and paste in the following code:

```python
import miniform

class MyGame(miniform.app.MiniApp):
    def __init__(self) -> None:
        super().__init__(
            title = "My Game",
            window_size = [800, 600],
        )

    def init(self) -> None: pass
    def exit(self) -> None: pass

    def update_hook(self, dt: float) -> None: pass
    def render_hook(self) -> None: pass

if __name__ == "__main__":
    MyGame().run()
```
| NOTE: The methods `init()`, `exit()` must be defined for any instance of `MiniApp`; a `NotImplementedError` is raised otherwise.

Above is the minimal code needed to get a simple `MiniApp` up and running. From here you can explore the `MiniWorld` and the other classes provided in `miniform.core.resource` and `miniform.core.resource.interface`.

## Contributions?  
Want to help improve **miniform**? Feel free to contribute by submitting issues, suggesting features, or making pull requests!  

## License  
**miniform** is open-source under the **MIT License.**
</div>
