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
            
    
    def update_units(self, sensor_mask, energies, types):
        for tile in self.map:
            tile.is_visible = sensor_mask[tile.position[0]][tile.position[1]]
            tile.energy = energies[tile.position[0]][tile.position[1]]
            tile.type = types[tile.position[0]][tile.position[1]]
            
            
    def update(self, obs: dict):
        unit_mask = np.array(obs["units_mask"][self.team_id])
        self.update_visibility(unit_mask)
        
        energies = np.array(obs["map_features"]["energy"])
        tile_types = np.array(obs["map_features"]["tile_type"])
        self.update_tiles(energies, tile_types)
        
        visible_relic_node_ids = np.where(unit_mask)[0]
        relic_positions = np.array(obs["relic_nodes"])
        self.update_relic_tiles(visible_relic_node_ids, relic_positions)
        
        unit_positions = np.array(obs["units"]["position"][self.team_id])
        unit_energys = np.array(obs["units"]["energy"][self.team_id])
        self.update_units()
               
    
    def update_map(self, obs: dict):
        unit_mask = np.array(obs["units_mask"][self.team_id]) # shape (max_units, )
        unit_positions = np.array(obs["units"]["position"][self.team_id]) # shape (max_units, 2)
        unit_energys = np.array(obs["units"]["energy"][self.team_id]) # shape (max_units, 1)
        observed_relic_node_positions = np.array(obs["relic_nodes"]) # shape (max_relic_nodes, 2)
        observed_relic_nodes_mask = np.array(obs["relic_nodes_mask"]) # shape (max_relic_nodes, )
        team_points = np.array(obs["team_points"]) # points of each team, team_points[self.team_id] is the points of the your team
        
        # ids of units you can control at this timestep
        available_unit_ids = np.where(unit_mask)[0]
        # visible relic nodes
        visible_relic_node_ids = set(np.where(observed_relic_nodes_mask)[0])
        
        sensor_mask = np.array(obs["units_mask"])
        
        actions = np.zeros((self.env_cfg["max_units"], 3), dtype=int)
        
        
        