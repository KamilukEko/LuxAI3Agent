import numpy as np
from models.tile_type import TileType

class MapManager:
    def __init__(self, team_id, width=24, height=24):
        self.team_id = team_id
        self.width = width
        self.height = height
        
        # Store relic nodes as a numpy array
        self.relic_nodes = []
        
        # Use numpy arrays for map data
        self.energy = np.full((width, height), -1)
        self.tile_type = np.full((width, height), TileType.UNKNOWN.value)
        self.has_relic = np.zeros((width, height), dtype=bool)
        self.is_visible = np.zeros((width, height), dtype=bool)
        
    def update_visibility(self, sensor_mask):
        """Update tile visibility based on sensor mask."""
        self.is_visible = np.array(sensor_mask)
    
    def update_relic_tiles(self, visible_relic_nodes, relic_positions):
        """Update relic node information."""
        for node_id in visible_relic_nodes:
            x, y = relic_positions[node_id]
            
            if 0 <= x < self.width and 0 <= y < self.height:
                self.has_relic[x, y] = True
                
                # Store relic node position if not already tracked
                relic_pos = np.array([x, y])
                if not any(np.array_equal(relic_pos, node) for node in self.relic_nodes):
                    self.relic_nodes.append(relic_pos)
    
    def update_tiles(self, energies, types):
        """Update tile energy and type for visible tiles."""
        # Only update visible tiles with valid data
        mask = self.is_visible & (energies != -1) & (types != -1)
        self.energy[mask] = energies[mask]
        self.tile_type[mask] = types[mask]
    
    def update(self, obs):
        """Update map state from observation."""
        # Update visibility
        sensor_mask = np.array(obs["sensor_mask"])
        self.update_visibility(sensor_mask)
        
        # Update tile data
        energies = np.array(obs["map_features"]["energy"])
        tile_types = np.array(obs["map_features"]["tile_type"])
        self.update_tiles(energies, tile_types)
        
        # Update relic nodes
        relic_nodes_mask = np.array(obs["relic_nodes_mask"])
        visible_relic_node_ids = np.where(relic_nodes_mask)[0]
        relic_positions = np.array(obs["relic_nodes"])
        self.update_relic_tiles(visible_relic_node_ids, relic_positions)
    
    def get_closest_relic_tile(self, position):
        """Find closest relic node using Manhattan distance."""
        if not self.relic_nodes:
            return None, 50
        
        position = np.array(position)
        distances = np.sum(np.abs(np.array(self.relic_nodes) - position), axis=1)
        
        if len(distances) > 0:
            min_idx = np.argmin(distances)
            return self.relic_nodes[min_idx], distances[min_idx]
        
        return None, 50