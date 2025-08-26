from miniform.imports import pg
import miniform

# tile_data = {tile_id, sheet_id, layer_id, flags}
# tile flags specify things like TILE_DYNAMIC, and TILE_ANIMATED etc...
# layer_id is utilized internally to render tiles in order
# sheet_id may reference a tile sheet or a sprite sheet, while tile_id is used to index into either

class MiniTilemap(miniform.MiniAtom):
    def __init__(
            self,
            world: "miniform.resource.world.MiniWorld",
            
            tile_size: list[int],
            tile_origin: list[int]=[0, 0],
            tile_color: list[int]=[172, 50, 50]) -> None:
        super().__init__()
        self.world: miniform.resource.world.MiniWorld = world
        self.configure(tile_size, tile_origin, tile_color)

    def configure(
            self,
            tile_size: list[int],
            tile_origin: list[int]=[0, 0],
            tile_color: list[int]=[172, 50, 50]) -> None:
        self.tile_size: list[int] = [*map(int, tile_size)]
        self.tile_color: list[int] = [*map(int, tile_color)]
        self.tile_origin: list[int] = [*map(int, tile_origin)]
        self.tile_data: dict[list, dict[str, int]] = {}

        self._freeze()

    def _serialize(self) -> dict:
        tile_size = self.tile_size
        tile_color = self.tile_color
        tile_origin = self.tile_origin

        tile_meta = []
        for key, tile_data in self.tile_data.items():
            tid, sid, lid, flags, obj = tile_data.values()
            tile_meta.append([obj.pos, tid, sid, lid, flags])        

        return {"tile-size": tile_size, "tile-color": tile_color, "tile-origin": tile_origin, "tile-meta": tile_meta}

    def get_tile_pos(self, pos: list[float]) -> tuple[int]:
        return tuple(miniform.utils.div2_v2i(miniform.utils.sub_v2(pos, self.tile_origin), self.tile_size))

    def set_tile(self, pos: list[int], tid: int, sid: int=0, lid: int=0, flags: int=0) -> None:
        tile_pos = self.get_tile_pos(pos)
        if (tile_data := (self.tile_data.get(tile_pos, None))) == None:
            
            tile_object = self.world.load_object(f"{tile_pos}", self.tile_size, miniform.utils.mul_v2i(tile_pos, self.tile_size), color=self.tile_color, static=not ((flags & miniform.MiniTileFlag.TILE_DYNAMIC) == miniform.MiniTileFlag.TILE_DYNAMIC))
            tile_data = {"tid": tid, "sid": sid, "lid": lid, "flags": flags, "object": tile_object}
            
            self.tile_data[tile_pos] = tile_data
            miniform.MiniLogger.debug(f"[MiniTilemap] set tile at: {tile_pos} {tile_data}")
        else: miniform.MiniLogger.warning(f"[MiniTilemap] tile exists at: {tile_pos} {tile_data}")

    def get_tile(self, pos: list[int]) -> dict:
        tile_pos = tuple(miniform.utils.div2_v2i(pos, self.tile_size))
        return self.tile_data.get(tile_pos, None)

    def pop_tile(self, pos: list[int]) -> dict:
        tile_pos = tuple(miniform.utils.div2_v2i(pos, self.tile_size))
        tile_data = self.get_tile(pos)
        if not tile_data: return

        self.world.unload_object(f"{tile_pos}")
        del self.tile_data[tile_pos]
        
        miniform.MiniLogger.debug(f"[MiniTilemap] popped tile at: {tile_pos} {tile_data}")
        return tile_data

    def rem_tile(self, pos: list[int]) -> None:
        tile_pos = tuple(miniform.utils.div2_v2i(pos, self.tile_size))
        tile_data = self.get_tile(pos)
        if not tile_data: return

        self.world.unload_object(f"{tile_pos}")
        
        miniform.MiniLogger.debug(f"[MiniTilemap] removed tile at: {tile_pos} {tile_data}")
        del self.tile_data[tile_pos]
