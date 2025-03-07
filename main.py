import json
import sys
from argparse import Namespace
import os

# switch it back to make it work
# from agent import Agent
from models.agent_base import AgentBase


from lux.kit import from_json

# This code comes directly from documentation and had to stay untouched. I did some minor changes to look prettier.

agent_dict = dict() # store potentially multiple dictionaries as kaggle imports code directly
agent_prev_obs = dict()

# Reads input from stdin
def read_input():
    try:
        return input()
    except EOFError as eof:
        raise SystemExit(eof)


def get_agents_response(observation, configurations):
    # Agent definition for kaggle submission.
    global agent_dict
    obs = observation.obs
    
    if type(obs) == str:
        obs = json.loads(obs)
        
    step = observation.step
    player = observation.player
    remainingOverageTime = observation.remainingOverageTime
    
    if step == 0:
        # agent_dict[player] = Agent(player, configurations["env_cfg"])
        agent_dict[player] = AgentBase(player, configurations["env_cfg"])

    if "__raw_path__" in configurations:
        dirname = os.path.dirname(configurations["__raw_path__"])
    else:
        dirname = os.path.dirname(__file__)

    sys.path.append(os.path.abspath(dirname))

    agent = agent_dict[player]
    actions = agent.act(step, from_json(obs), remainingOverageTime)
    return dict(action=actions.tolist())


if __name__ == "__main__":
    step = 0
    player_id = 0
    env_cfg = None
    i = 0
    while True:
        inputs = read_input()
        raw_input = json.loads(inputs)
        observation = Namespace(**dict(step=raw_input["step"], obs=raw_input["obs"], remainingOverageTime=raw_input["remainingOverageTime"], player=raw_input["player"], info=raw_input["info"]))
        
        if i == 0:
            env_cfg = raw_input["info"]["env_cfg"]
            player_id = raw_input["player"]
            
        i += 1
        actions = get_agents_response(observation, dict(env_cfg=env_cfg))
        
        # Send actions to engine
        print(json.dumps(actions))