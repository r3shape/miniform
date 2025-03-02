from r3frame.objects.game.base import Game_Object

class Chain:
    def __init__(self, root: Game_Object, links: list[Game_Object], link_offset: list[int | float] = [0, 0]) -> None:
        self.root = root
        self.links = links
        self.link_offset = link_offset
        self.link()

    def link(self) -> None:
        """Set link positions based on root."""
        prev = self.root
        for link in self.links:
            link.location = [prev.location[0] + self.link_offset[0], prev.location[1] + self.link_offset[1]]
            prev = link

    def set_link(self, obj: Game_Object) -> None:
        """Sets an object to the end of the chain."""
        self.links.append(obj)
        prev = self.links[-1] if self.links else self.root
        obj.location = [prev.location[0] + self.link_offset[0], prev.location[1] + self.link_offset[1]]

    def rem_link(self) -> Game_Object|None:
        """Remove and return an object from the end of the chain."""
        if self.links:
            obj = self.links.pop()
            self.links.remove(obj)
            return obj
        else: return None

    def get_objects(self) -> list[Game_Object]:
        """ Returns a list of all objects in the chain, including the root."""
        return [self.root, *self.links]

    @staticmethod
    def get_scaling(index: int, parent: Game_Object, link: Game_Object) -> float:
        """Default scaling factor applied to link velocity updates. Override this for different chain behaviors."""
        return 10 / (index + 1)

    def update(self, delta_time: float) -> None:
        """ Updates each member of the chain using inverse kinematics."""
        self.root.update(delta_time)
        for i, link in enumerate(self.links):
            parent = self.root if i == 0 else self.links[i - 1]
            link.velocity = [
                (parent.location[0] - (link.location[0] + self.link_offset[0])) * self.get_scaling(i, parent, link),
                (parent.location[1] - (link.location[1] + self.link_offset[1])) * self.get_scaling(i, parent, link),
            ]
            link.update(delta_time)

    def debug_render(self, renderer) -> None:
        """ Renders a debug visualization of the chain. """
        prev = self.root
        for link in self.links:
            renderer.draw_circle([link.location[0] + link.size[0] / 2 , link.location[1] + link.size[1] / 2], link.size[0], [255, 255, 255], 1)
            renderer.draw_line(
                [prev.location[0] + prev.size[0] / 2, prev.location[1] + prev.size[1] / 2],
                [link.location[0] + link.size[0] / 2, link.location[1] + link.size[1] / 2], 
                [255, 0, 0], 3
            )
            prev = link
