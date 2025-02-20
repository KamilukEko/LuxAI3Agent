import numpy as np
from models.map import Map
from models.tile_type import TileType
from models.map_tile import MapTile
from lux.utils import calculate_manhattan_distance

class MapManager:
    def __init__(self, team_id):
        #id of the team that uses the MapManager
        self.team_id = team_id 
        # position of relic nodes observed by the team
        self.relic_nodes = [] 
        # map that holds states of the reconessances
        self.map = Map() 
        
        
    def update_visibility(self, sensor_mask):
        """Based on the results of vision of units in given round it updated whetever tile is visible for the team or not.

        Args:
            sensor_mask (_type_): _description_
        """
        for tile in self.map:
           tile.is_visible = sensor_mask[tile.position[0], tile.position[1]]
           
        
    def update_relic_tiles(self, visible_relic_nodes, relic_positions):
        for node_id in visible_relic_nodes:
            x = relic_positions[node_id][0]
            y = relic_positions[node_id][1]
            tile = self.map[x, y]
            
            if tile is not None:
                tile.has_relic = True
                if tile not in self.relic_nodes:
                    self.relic_nodes.append(tile)
            else:
                pass
                # with open('relic_debug.txt', 'a+') as f:
                #     f.write(f"Ostrzeżenie: Brak kafelka na pozycji ({x}, {y})\n")
    
    
    def update_tiles(self, energies, types):
        """Update the state of the tiles on the map (as tiles change their types and energies every round)

        Args:
            energies (_type_): _description_
            types (_type_): _description_
        """
        for tile in self.map:
            # state of the tile can be changed only if it is visible, otherwise we don't know what is happening
            if tile.is_visible:
                tile.energy = energies[tile.position[0]][tile.position[1]]
                tile.type = TileType(types[tile.position[0]][tile.position[1]])
            
    
    def update_units(self, units):
        for tile in self.map:
            tile.units = []
            for unit in units:
                if np.all(unit.position == tile.position):
                    tile.units.append(unit)
            
    def update(self, obs: dict):
        unit_mask = np.array(obs["units_mask"][self.team_id])
        sensor_mask = np.array(obs["sensor_mask"])
        self.update_visibility(sensor_mask)

        energies = np.array(obs["map_features"]["energy"])
        tile_types = np.array(obs["map_features"]["tile_type"])
        self.update_tiles(energies, tile_types)
        
        # Użyj maski relikvii zamiast maski jednostek
        relic_nodes_mask = np.array(obs["relic_nodes_mask"])
        visible_relic_node_ids = np.where(relic_nodes_mask)[0]
        relic_positions = np.array(obs["relic_nodes"])
        self.update_relic_tiles(visible_relic_node_ids, relic_positions)

    def get_closest_relic_tile(self, position) -> MapTile:
        """Receives position and finds the closest MapTile with relic node with respect to Manhattan Distance

        Args:
            position (_type_): X and Y coordinates

        Returns:
            MapTile: _description_ or None if no found
        """

        current_closest_relic_node, distance_to_current_closest_relic_node = None, 50
        for relic_node in self.relic_nodes:
            mh_distance_to_relic_node = calculate_manhattan_distance(position, relic_node.position)
            if mh_distance_to_relic_node < distance_to_current_closest_relic_node:
                distance_to_current_closest_relic_node = mh_distance_to_relic_node
                current_closest_relic_node = relic_node

        return current_closest_relic_node, distance_to_current_closest_relic_node
        
        