# Lux AI Challenge S3 - NEURAL.WZIM

## Project setup:
1. Create clear conda environemnt
```
conda create -n s3-lux-ai-chall
```
2. Acticate the environment
```
conda activate s3-lux-ai-chall
```
3. Install dependencies
```
conda install --file requirements.txt
```

Then everytime you work on the project use code below before execution of the code 
```
conda activate s3-lux-ai-chall
```

## Directories
- `/lux` - directory with auxiliary tools
    - `/lux/kit.py` - module with tools for JSON serialzation/un-serialization
    - `/lux/utils.py` - module with basic function for units movement and calculating manhattan distance
- `/models` - directory with classes that represent environment components + agent
    - `/models/agent_base.py` - class that defines the agent that is decision maker and learner, uses services to understand the state of the environment and take appropriate actions
    - `/models/map.py` - class that defines the map that is being used by map manager
    - `/models/tile_type.py` - class that defines the structure of the tiles of the map (as there are many types)
    - `/models/unit.py` - class that defines the atomic unit that is subject to actions by agent
- `/services` - directory with classes that receive and map changes in the components (from `/models` directory) based on inputs from game engine
    - `/services/map_manager.py` - class that manages changes on the map
    - `/services/unit_manager.py` - class that manages changes in the units
- `/main.py` - main file that allows agent to play the game
- `/tournament_mt.py` - file that allows to check performance of two agents (win ratio)

## Usage
To run the 5-round match against two agents use:
```
luxai-s3 path/to/bot_0/main.py path/to/bot_1/main.py --output replay.json
```

To measure the performance between two bots (can be self) use:
```
python tournament_mt.py path/to/bot_0/main.py path/to/bot_1/main.py -n <number of 5-round matches> -w <number of cores>
```