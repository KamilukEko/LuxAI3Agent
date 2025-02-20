import numpy as np

# direction (0 = center, 1 = up, 2 = right, 3 = down, 4 = left)
def direction_to(src, target):
    with open('direction_debug.txt', 'a+') as f:
        f.write(f"src: {src}, type: {type(src)}, shape: {getattr(src, 'shape', 'no shape')}\n")
        f.write(f"target: {target}, type: {type(target)}, shape: {getattr(target, 'shape', 'no shape')}\n")
        
        # Próba wykonania operacji
        try:
            ds = target - src
            f.write(f"ds: {ds}, type: {type(ds)}, shape: {getattr(ds, 'shape', 'no shape')}\n")
            
            dx = ds[0]
            dy = ds[1]
            f.write(f"dx: {dx}, type: {type(dx)}, shape: {getattr(dx, 'shape', 'no shape')}\n")
            f.write(f"dy: {dy}, type: {type(dy)}, shape: {getattr(dy, 'shape', 'no shape')}\n")
            
            # Poprawka warunku
            if isinstance(dx, (int, float)):
                center_condition = (dx == 0 and dy == 0)
            else:
                center_condition = (np.all(dx == 0) and np.all(dy == 0))
                
            f.write(f"center_condition: {center_condition}\n")
            
            if center_condition:
                return 0
                
            # Dalszy kod bez zmian
            if abs(dx) > abs(dy):
                if dx > 0:
                    return 2 
                else:
                    return 4
            else:
                if dy > 0:
                    return 3
                else:
                    return 1
                    
        except Exception as e:
            f.write(f"ERROR in direction_to: {str(e)}\n")
            # Zwróć domyślny kierunek w przypadku błędu
            return 0
        
def calculate_manhattan_distance(X, Y) -> int:
    """Takes two N-dimensional points and returns Manhattan distance between them

    Args:
        X (two-dimensional iterable): first point
        Y (two-dimensional iterable): second point

    Returns:
        int: mahattan distance
    """

    if(isinstance(X, np.ndarray) and isinstance(Y, np.ndarray)):
        if X.shape == Y.shape:
            return np.abs(X - Y).sum()
        else:
            raise ValueError("Shapes of the structures differ, thus we can't calculate the Manhattan distance")
    elif(isinstance(X, list) and isinstance(Y, list)):
        if len(X) == len(Y):
            return sum([np.abs(x - y) for x, y in zip(X, Y)])
        else:
            raise ValueError("Shapes of the structures differ, thus we can't calculate the Manhattan distance")
    elif((isinstance(X, list) and isinstance(Y, np.ndarray)) or (isinstance(Y, list) and isinstance(X, np.ndarray))):
        if len(X) == len(Y):
            return sum([np.abs(x - y) for x, y in zip(list(X), list(Y))])
        else:
            raise ValueError("Shapes of the structures differ, thus we can't calculate the Manhattan distance")
    else:
        raise TypeError("The structures differ in types, can't reliably compute Manhattan distance")
