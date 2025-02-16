import numpy as np
from models.map import Map
from models.tile_type import TileType


class MapManager:
    def __init__(self, team_id):
        self.team_id = team_id
        self.map = Map()
        
        
    def update_visibility(self, sensor_mask):
       for tile in self.map:
           tile.is_visible = sensor_mask[tile.position[0], tile.position[1]]
           
        
    def update_relic_tiles(self, visible_relic_nodes, relic_positions):
       for node_id in visible_relic_nodes:
            tile = self.map[relic_positions[node_id][0], relic_positions[node_id][1]]
            tile.has_relic = True
    
    
    def update_tiles(self, energies, types):
        for tile in self.map:
            if tile.is_visible:
                tile.energy = energies[tile.position[0]][tile.position[1]]
                tile.type = TileType(types[tile.position[0]][tile.position[1]])
            
    
    def update_units(self, units):
        for tile in self.map:
            tile.units = []
            for unit in units:
                if unit.position == tile.position:
                    tile.units.append(units.pop(unit))
            
            
    def update(self, obs: dict):
        unit_mask = np.array(obs["units_mask"][self.team_id])
        self.update_visibility(unit_mask)
        
        energies = np.array(obs["map_features"]["energy"])
        tile_types = np.array(obs["map_features"]["tile_type"])
        self.update_tiles(energies, tile_types)
        
        visible_relic_node_ids = np.where(unit_mask)[0]
        relic_positions = np.array(obs["relic_nodes"])
        self.update_relic_tiles(visible_relic_node_ids, relic_positions)
        
        