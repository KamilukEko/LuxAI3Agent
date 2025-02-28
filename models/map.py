import numpy as np
from models.tile_type import TileType

class Map:
    def __init__(self, width=24, height=24):
        # Use numpy arrays for all tile properties instead of objects
        self.width = width
        self.height = height
        
        # Initialize arrays with default values
        self.energy = np.full((width, height), -1)
        self.tile_type = np.full((width, height), TileType.UNKNOWN.value)
        self.has_relic = np.zeros((width, height), dtype=bool)
        self.is_visible = np.zeros((width, height), dtype=bool)
        
        # Track units separately using a list for each position
        self.units = [[[] for _ in range(height)] for _ in range(width)]
    
    def __getitem__(self, key):
        """Access properties for a coordinate as a tuple."""
        if isinstance(key, tuple) and len(key) == 2:
            x, y = key
            if 0 <= x < self.width and 0 <= y < self.height:
                return {
                    'position': (x, y),
                    'energy': self.energy[x, y],
                    'tile_type': TileType(self.tile_type[x, y]),
                    'has_relic': self.has_relic[x, y],
                    'is_visible': self.is_visible[x, y],
                    'units': self.units[x][y]
                }
        return None
    
    def get_all_positions(self):
        """Get all map positions as a list of tuples."""
        return [(x, y) for x in range(self.width) for y in range(self.height)]
    
    def update_tile(self, x, y, properties):
        """Update properties for a specific tile."""
        if 'energy' in properties:
            self.energy[x, y] = properties['energy']
        if 'tile_type' in properties:
            self.tile_type[x, y] = properties['tile_type'].value if hasattr(properties['tile_type'], 'value') else properties['tile_type']
        if 'has_relic' in properties:
            self.has_relic[x, y] = properties['has_relic']
        if 'is_visible' in properties:
            self.is_visible[x, y] = properties['is_visible']