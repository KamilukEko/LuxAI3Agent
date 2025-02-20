import numpy as np
from models.unit import Unit


class UnitsManager:
    def __init__(self, team_id, map_manager):
        self.map_manager = map_manager
        self.team_id = team_id
        self.enemy_units: list[Unit] = []
        self.friendly_units: list[Unit] = []
        
    def has_exploration_target(self, unit_id):
        return hasattr(self.friendly_units[unit_id], 'exploration_target') and self.friendly_units[unit_id].exploration_target is not None

    def set_exploration_target(self, unit_id, location):
        self.friendly_units[unit_id].exploration_target = location

    def get_exploration_target(self, unit_id):
        return self.friendly_units[unit_id].exploration_target
        
    def update_units(self, positions, energies, team_id):
        # with open('units_debug.txt', 'a+') as f:
        #     f.write(f"\n--- Update Units Team {team_id} ---\n")
        #     f.write(f"positions: {positions}, type: {type(positions)}, shape: {getattr(positions, 'shape', 'no shape')}\n")
        #     f.write(f"energies: {energies}, type: {type(energies)}, shape: {getattr(energies, 'shape', 'no shape')}\n")
        
        is_friendly = team_id == self.team_id
        units_list = self.friendly_units if is_friendly else self.enemy_units
        
        try:
            # Upewnij się, że positions jest przetwarzane poprawnie
            if isinstance(positions, tuple):
                # with open('units_debug.txt', 'a+') as f:
                #     f.write("Positions is a tuple, extracting first element\n")
                positions = positions[0]
                
            units_amount = len(positions)
            
            with open('units_debug.txt', 'a+') as f:
                f.write(f"units_amount: {units_amount}\n")
                
            for unit_id in range(units_amount):
                position = positions[unit_id]
                energy = energies[unit_id]
                
                # with open('units_debug.txt', 'a+') as f:
                #     f.write(f"unit_id: {unit_id}, position: {position}, energy: {energy}\n")
                    
                # Upewnij się, że pozycja ma poprawny format
                if isinstance(position, np.ndarray) and position.ndim > 1:
                    position = position.flatten()[:2]
                    # with open('units_debug.txt', 'a+') as f:
                    #     f.write(f"Flattened position: {position}\n")
                
                if unit_id >= len(units_list):
                    units_list.append(Unit(energy, position, is_friendly))
                    # with open('units_debug.txt', 'a+') as f:
                    #     f.write(f"Added new unit {unit_id}\n")
                else:
                    units_list[unit_id].update(energy, position)
                    # with open('units_debug.txt', 'a+') as f:
                    #     f.write(f"Updated unit {unit_id}\n")
                        
        except Exception as e:
            pass
            # with open('units_debug.txt', 'a+') as f:
            #     f.write(f"ERROR in update_units: {str(e)}\n")
            
            
    def update(self, obs: dict):
        for team_id in range(2):     
            unit_positions = np.array(obs["units"]["position"][team_id])
            unit_energies = np.array(obs["units"]["energy"][team_id])
            self.update_units(unit_positions, unit_energies, team_id)
            
        self.map_manager.update_units(self.friendly_units + self.enemy_units)
               

    def __getitem__(self, unit_id):
        if isinstance(unit_id, int):
            if unit_id < 0 or unit_id >= len(self.friendly_units):
                raise KeyError(f"The unit does not exist in the manager. The key is either too high or too low for. (Tried {unit_id} for sequence of units of length {len(self.friendly_units)})")
            else:
                return self.friendly_units[unit_id]
        else:
            raise TypeError(f"Passed wrong type of key to select the unit. Make sure to pass non-negative integers that are lower than amount of units at the moment ({len(self.friendly_units)})")
        