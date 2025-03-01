class Unit:
    def __init__(self, energy, position, is_friendly) -> None:
        self.energy = energy
        self.position = position
        self.is_friendly = is_friendly
        self.exploration_target = None
        
    def update(self, energy, position):
        self.energy = energy
        self.position = position
        