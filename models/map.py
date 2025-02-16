from models.map_tile import MapTile


class Map:
    def __init__(self):
        self.tiles = [MapTile([x, y]) for x in range(24) for y in range(24)]
       
        
    def __getitem__(self, x, y):
        for tile in self.tiles:
            if tile.position == [x, y]:
                return tile
            
    
    def __iter__(self):
        return iter(self.tiles)