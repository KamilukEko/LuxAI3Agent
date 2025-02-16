import numpy as np
from models.unit import Unit


class UnitsManager:
    def __init__(self, team_id, map_manager):
        self.map_manager = map_manager
        self.team_id = team_id
        self.enemy_units: list[Unit] = []
        self.friendly_units: list[Unit] = []
        
    
    def update_units(self, positions, energies, team_id):
        is_friendly = team_id == self.team_id
        units_list = self.friendly_units if is_friendly else self.enemy_units
        units_amount = len(positions)
        
        for unit_id in range(units_amount):
            if unit_id >= len(units_list):
                units_list.append(Unit(energies[unit_id], positions[unit_id], is_friendly))
            else:
                units_list[unit_id].update(energies[unit_id], positions[unit_id])
            
            
    def update(self, obs: dict):
        for team_id in range(2):     
            unit_positions = np.array(obs["units"]["position"][team_id]), 
            unit_energies = np.array(obs["units"]["energy"][team_id])
            self.update_units(unit_positions, unit_energies, team_id)
            
        self.map_manager.update_units(self.friendly_units + self.enemy_units)
               

        
        
        