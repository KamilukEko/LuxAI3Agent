import numpy as np
from services.map_manager import MapManager
from services.units_manager import UnitsManager
from lux.utils import direction_to


class AgentBase:
    def __init__(self, player: str, env_cfg) -> None:
        self.player = player
        self.opp_player = "player_1" if self.player == "player_0" else "player_0"
        self.team_id = 0 if self.player == "player_0" else 1
        self.opp_team_id = 1 if self.team_id == 0 else 0
        np.random.seed(0)
        
        self.env_cfg = env_cfg
        
        self.map_manager = MapManager(self.team_id)
        self.units_manager = UnitsManager(self.team_id, self.map_manager)
        
    
    def update_states(self, obs: dict):
        """Update the states of the map and units to make reasonable moves

        Args:
            obs (dict): dictionary with the current round input
        """
        self.map_manager.update(obs)
        self.units_manager.update(obs)
        
    
    def prepare_actions(self, step: int, remainingOverageTime: int = 60):
        # with open('actions_debug.txt', 'a+') as f:
        #     f.write(f"\n--- Prepare Actions Step {step} ---\n")
        #     f.write(f"Friendly units count: {len(self.units_manager.friendly_units)}\n")
        
        actions = np.zeros((self.env_cfg["max_units"], 3), dtype=int)
            
        for unit_id, unit in enumerate(self.units_manager.friendly_units):
            unit_pos = unit.position
            unit_energy = unit.energy
            
            # with open('actions_debug.txt', 'a+') as f:
            #     f.write(f"unit_id: {unit_id}, position: {unit_pos}, type: {type(unit_pos)}, energy: {unit_energy}\n")

            closest_relic, distance_to_closest_relic = self.map_manager.get_closest_relic_tile(unit_pos)
            
            # with open('actions_debug.txt', 'a+') as f:
            #     f.write(f"closest_relic: {closest_relic}, distance: {distance_to_closest_relic}\n")
            
            if closest_relic is not None:
                # if close to the relic node we want to hover around it
                if distance_to_closest_relic <= 4:
                    random_direction = np.random.randint(0, 5)
                    actions[unit_id] = [random_direction, 0, 0]
                    # with open('actions_debug.txt', 'a+') as f:
                    #     f.write(f"near relic - random move: {random_direction}\n")
                else:
                    # move towards relic
                    relic_pos = closest_relic.position
                    # with open('actions_debug.txt', 'a+') as f:
                    #     f.write(f"relic_pos: {relic_pos}, type: {type(relic_pos)}\n")
                        
                    try:
                        direction = direction_to(unit_pos, relic_pos)
                        actions[unit_id] = [direction, 0, 0]
                        # with open('actions_debug.txt', 'a+') as f:
                        #     f.write(f"move to relic direction: {direction}\n")
                    except Exception as e:
                        # with open('actions_debug.txt', 'a+') as f:
                        #     f.write(f"ERROR moving to relic: {str(e)}\n")
                        actions[unit_id] = [0, 0, 0]  # domyślnie nie ruszaj się
            else:
                # random exploration
                try:
                    if step % 20 == 0 or not self.units_manager.has_exploration_target(unit_id):
                        rand_loc = (np.random.randint(0, self.env_cfg["map_width"]), 
                            np.random.randint(0, self.env_cfg["map_height"]))
                        self.units_manager.set_exploration_target(unit_id, rand_loc)
                        # with open('actions_debug.txt', 'a+') as f:
                        #     f.write(f"new exploration target: {rand_loc}\n")
                    
                    target_loc = self.units_manager.get_exploration_target(unit_id)
                    # with open('actions_debug.txt', 'a+') as f:
                    #     f.write(f"target_loc: {target_loc}, type: {type(target_loc)}\n")
                        
                    direction = direction_to(unit_pos, target_loc)
                    actions[unit_id] = [direction, 0, 0]
                    # with open('actions_debug.txt', 'a+') as f:
                    #     f.write(f"exploration direction: {direction}\n")
                except Exception as e:
                    pass
                    # with open('actions_debug.txt', 'a+') as f:
                    #     f.write(f"ERROR in exploration: {str(e)}\n")
                    actions[unit_id] = [0, 0, 0]  # domyślnie nie ruszaj się

        return actions

    
    def act(self, step: int, obs: dict, remainingOverageTime: int = 60):
        # important distinction here, the update_states uses the information to lay it down on the static structures
        self.update_states(obs)
        # the act component prepares the action without need to look at what happened as it makes its decision solely based on remembered states
        return self.prepare_actions(step, remainingOverageTime)
    