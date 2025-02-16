from models.tile_type import TileType


class MapTile:
    def __init__(self, position) -> None:
        self.position = position
        self.energy = -1
        self.tile_type = TileType.UNKNOWN
        
        self.has_relic = False
        self.is_visible = False
        self.units = []
        