import os
import sys
import subprocess
import re
import numpy as np
from scipy import stats
import concurrent.futures
import time
from tqdm import tqdm
import argparse

# Wilson confidence interval calculation
def wilson_interval(successes, n, confidence=0.95):
    """
    Calculate Wilson confidence interval for a proportion.
    
    Parameters:
    - successes: number of successes
    - n: sample size
    - confidence: confidence level (default 0.95)
    
    Returns:
    - (lower, upper): confidence interval bounds
    """
    if n == 0:
        return 0, 0
    
    p_hat = successes / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    z2 = z**2
    
    # Standard Wilson interval
    denom = 1 + z2 / n
    center = p_hat + z2 / (2 * n)
    pm = z * np.sqrt(p_hat * (1 - p_hat) / n + z2 / (4 * n**2))
    lower = max(0, (center - pm) / denom)
    upper = min(1, (center + pm) / denom)
    
    return lower, upper

def run_match(args):
    """Run a single match between two agents."""
    game_id, agent1_path, agent2_path, seed = args
    
    # Create command with seed
    cmd = ["luxai-s3", agent1_path, agent2_path, "--seed", str(seed)]
    
    try:
        # Run the match and capture output
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        end_time = time.time()
        
        if result.returncode != 0:
            print(f"Error in game {game_id}: {result.stderr[:200]}...")
            return game_id, None, end_time - start_time
        
        # Parse the result to find the winner
        output = result.stdout
        pattern = r"'(player_\d+)':\s*array\((\d+),\s*dtype=int32\)"
        
        # Find all matches in the text
        matches = re.findall(pattern, output)
        
        # Convert to dictionary with player as key and array value as integer
        match_result = {player: int(value) for player, value in matches}
        
        # Check if player_0 won (3 or more match wins)
        player_0_won = 1 if match_result.get("player_0", 0) >= 3 else 0
        
        return game_id, player_0_won, end_time - start_time
        
    except subprocess.TimeoutExpired:
        print(f"Game {game_id} timed out after 300 seconds")
        return game_id, None, 300
    except Exception as e:
        print(f"Error in game {game_id}: {str(e)}")
        return game_id, None, 0

def run_parallel_tournament(agent1_path, agent2_path, num_games, max_workers=None, starting_seed=42):
    """Run multiple games in parallel using process pool."""
    
    # Prepare arguments for each game
    game_args = [(i, agent1_path, agent2_path, starting_seed + i) for i in range(num_games)]
    
    results = np.zeros(num_games)
    times = []
    completed = 0
    
    # Use ProcessPoolExecutor for parallelism
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and create a map of futures to game IDs
        future_to_game = {executor.submit(run_match, args): args[0] for args in game_args}
        
        # Process results as they complete
        for future in tqdm(concurrent.futures.as_completed(future_to_game), total=num_games, desc="Running games"):
            game_id, result, elapsed_time = future.result()
            if result is not None:
                results[game_id] = result
                times.append(elapsed_time)
                completed += 1
    
    return results, times, completed

def main():
    parser = argparse.ArgumentParser(description="Run a parallel tournament between two Lux AI agents")
    parser.add_argument("agent1", help="Path to the first agent's main.py file")
    parser.add_argument("agent2", help="Path to the second agent's main.py file")
    parser.add_argument("-n", "--num-games", type=int, default=10, help="Number of games to run")
    parser.add_argument("-w", "--workers", type=int, default=None, 
                       help="Maximum number of worker processes (default: CPU count)")
    parser.add_argument("-s", "--seed", type=int, default=42, help="Starting seed for games")
    parser.add_argument("-c", "--confidence", type=float, default=0.95,
                       help="Confidence level for interval calculation (default: 0.95)")
    
    args = parser.parse_args()
    
    print(f"Running {args.num_games} games between:")
    print(f"Player 0: {args.agent1}")
    print(f"Player 1: {args.agent2}")
    print(f"Using up to {args.workers if args.workers else 'CPU count'} parallel processes")
    
    # Run the tournament
    start_time = time.time()
    results, game_times, completed = run_parallel_tournament(
        args.agent1, args.agent2, args.num_games, args.workers, args.seed
    )
    total_time = time.time() - start_time
    
    # Calculate statistics
    if completed > 0:
        successes = np.sum(results)
        win_rate = successes / completed
        conf_interval_l, conf_interval_u = wilson_interval(successes, completed, args.confidence)
        
        print(f"\n🏆 Tournament Results:")
        print(f"Completed games: {completed}/{args.num_games}")
        print(f"Player 0 wins: {int(successes)} ({win_rate*100:.1f}%)")
        print(f"Player 1 wins: {completed - int(successes)} ({(1-win_rate)*100:.1f}%)")
        print(f"Win rate confidence interval: ({conf_interval_l:.4f}, {conf_interval_u:.4f}) with {args.confidence*100}% confidence")
        
        if game_times:
            avg_time = sum(game_times) / len(game_times)
            print(f"\n⏱️ Performance:")
            print(f"Average game time: {avg_time:.2f}s")
            print(f"Min game time: {min(game_times):.2f}s")
            print(f"Max game time: {max(game_times):.2f}s")
            print(f"Total wall-clock time: {total_time:.2f}s")
            print(f"Time saved through parallelization: {sum(game_times) - total_time:.2f}s")
    else:
        print("No games completed successfully.")

if __name__ == "__main__":
    main()