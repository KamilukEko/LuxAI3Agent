from services.map_manager import MapManager


class AgentBase:
    def __init__(self, player: str, env_cfg) -> None:
        self.player = player
        self.opp_player = "player_1" if self.player == "player_0" else "player_0"
        self.team_id = 0 if self.player == "player_0" else 1
        self.opp_team_id = 1 if self.team_id == 0 else 0
        
        self.env_cfg = env_cfg
        
        self.map_manager = MapManager()


    def update_state(self, step: int, obs: dict):
        pass
    
    
    def act(self, step: int, obs: dict):
        self.map_manager.update(obs)
        pass
    