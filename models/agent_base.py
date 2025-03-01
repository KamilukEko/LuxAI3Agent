import numpy as np

class AgentBase:
    def __init__(self, player: str, env_cfg) -> None:
        self.player = player
        self.opp_player = "player_1" if self.player == "player_0" else "player_0"
        self.team_id = 0 if self.player == "player_0" else 1
        self.opp_team_id = 1 if self.team_id == 0 else 0
        np.random.seed(0)
        
        self.env_cfg = env_cfg
        
        # Initialize managers with environment configuration
        from services.map_manager import MapManager
        from services.units_manager import UnitsManager
        
        self.map_manager = MapManager(self.team_id, env_cfg["map_width"], env_cfg["map_height"])
        self.units_manager = UnitsManager(self.team_id, self.map_manager)
        self.units_manager.max_units = env_cfg["max_units"]
    
    def update_states(self, obs: dict):
        """Update the states of the map and units."""
        self.map_manager.update(obs)
        self.units_manager.update_units(obs)
    
    def prepare_actions(self, step: int, remainingOverageTime: int = 60):
        """Prepare actions for all units based on current state."""
        actions = np.zeros((self.env_cfg["max_units"], 3), dtype=int)
        
        # Get available friendly units
        friendly_units = self.units_manager.get_friendly_units()
        
        for unit_id in friendly_units:
            unit_pos = self.units_manager.friendly_positions[unit_id]
            
            # Find closest relic
            closest_relic, distance_to_closest_relic = self.map_manager.get_closest_relic_tile(unit_pos)
            
            if closest_relic is not None:
                # If close to relic node, hover around it
                if distance_to_closest_relic <= 4:
                    random_direction = np.random.randint(0, 5)
                    actions[unit_id] = [random_direction, 0, 0]
                else:
                    # Move towards relic
                    from lux.utils import direction_to
                    direction = direction_to(unit_pos, closest_relic)
                    actions[unit_id] = [direction, 0, 0]
            else:
                # Random exploration
                if step % 20 == 0 or not self.units_manager.has_exploration_target(unit_id):
                    rand_loc = (np.random.randint(0, self.env_cfg["map_width"]), 
                        np.random.randint(0, self.env_cfg["map_height"]))
                    self.units_manager.set_exploration_target(unit_id, rand_loc)
                
                target_loc = self.units_manager.get_exploration_target(unit_id)
                if target_loc is not None:
                    from lux.utils import direction_to
                    direction = direction_to(unit_pos, target_loc)
                    actions[unit_id] = [direction, 0, 0]
                else:
                    actions[unit_id] = [0, 0, 0]  # Default to no movement

        return actions
    
    def act(self, step: int, obs: dict, remainingOverageTime: int = 60):
        """Process observations and return actions."""
        self.update_states(obs)
        return self.prepare_actions(step, remainingOverageTime)