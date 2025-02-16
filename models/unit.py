class Unit:
    def __init__(self, energy, position, is_friendly) -> None:
        self.energy = energy
        self.position = position
        self.is_friendly = is_friendly
        
    def update(self, energy, position):
        self.energy = energy
        self.position = position
        