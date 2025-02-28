import numpy as np

# direction (0 = center, 1 = up, 2 = right, 3 = down, 4 = left)
def direction_to(src, target):
    """Determine the direction to move from src to target.
    
    Returns:
    0 = center, 1 = up, 2 = right, 3 = down, 4 = left
    """
    try:
        ds = np.array(target) - np.array(src)
        
        # Check if we're already at the target
        if np.all(ds == 0):
            return 0
            
        # Determine primary direction
        if abs(ds[0]) > abs(ds[1]):
            return 2 if ds[0] > 0 else 4
        else:
            return 3 if ds[1] > 0 else 1
    except:
        # Default to no movement if something goes wrong
        return 0
        
def calculate_manhattan_distance(X, Y):
    """Calculate Manhattan distance between two points efficiently."""
    X = np.array(X)
    Y = np.array(Y)
    return np.sum(np.abs(X - Y))
