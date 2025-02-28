import numpy as np

class UnitsManager:
    def __init__(self, team_id, map_manager):
        self.team_id = team_id
        self.map_manager = map_manager
        
        # Use numpy arrays for unit properties instead of objects
        self.max_units = 100  # This should be set from env_cfg
        
        # Initialize arrays for friendly units
        self.friendly_positions = np.full((self.max_units, 2), -1)
        self.friendly_energies = np.full((self.max_units), -1)
        self.friendly_exploration_targets = np.full((self.max_units, 2), -1)
        self.friendly_exists = np.zeros(self.max_units, dtype=bool)
        
        # Initialize arrays for enemy units
        self.enemy_positions = np.full((self.max_units, 2), -1)
        self.enemy_energies = np.full((self.max_units), -1)
        self.enemy_exists = np.zeros(self.max_units, dtype=bool)
        
    def has_exploration_target(self, unit_id):
        return self.friendly_exists[unit_id] and np.all(self.friendly_exploration_targets[unit_id] != -1)

    def set_exploration_target(self, unit_id, location):
        if self.friendly_exists[unit_id]:
            self.friendly_exploration_targets[unit_id] = np.array(location)

    def get_exploration_target(self, unit_id):
        if self.friendly_exists[unit_id]:
            return self.friendly_exploration_targets[unit_id]
        return None
    
    def update_units(self, obs):
        # Update friendly units
        friendly_mask = np.array(obs["units_mask"][self.team_id])
        friendly_positions = np.array(obs["units"]["position"][self.team_id])
        friendly_energies = np.array(obs["units"]["energy"][self.team_id])
        
        # Reset existence flags
        self.friendly_exists.fill(False)
        
        # Update friendly units that exist
        available_unit_ids = np.where(friendly_mask)[0]
        for unit_id in available_unit_ids:
            if unit_id < self.max_units:
                self.friendly_exists[unit_id] = True
                self.friendly_positions[unit_id] = friendly_positions[unit_id]
                self.friendly_energies[unit_id] = friendly_energies[unit_id]
        
        # Update enemy units
        enemy_team_id = 1 - self.team_id
        enemy_mask = np.array(obs["units_mask"][enemy_team_id])
        enemy_positions = np.array(obs["units"]["position"][enemy_team_id])
        enemy_energies = np.array(obs["units"]["energy"][enemy_team_id])
        
        # Reset existence flags
        self.enemy_exists.fill(False)
        
        # Update enemy units that exist
        available_enemy_ids = np.where(enemy_mask)[0]
        for unit_id in available_enemy_ids:
            if unit_id < self.max_units:
                self.enemy_exists[unit_id] = True
                self.enemy_positions[unit_id] = enemy_positions[unit_id]
                self.enemy_energies[unit_id] = enemy_energies[unit_id]
                
    def get_friendly_units(self):
        """Return list of existing friendly unit IDs."""
        return np.where(self.friendly_exists)[0]
    
    def get_enemy_units(self):
        """Return list of existing enemy unit IDs."""
        return np.where(self.enemy_exists)[0]