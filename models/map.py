from models.map_tile import MapTile
import numpy as np

class Map:
    def __init__(self):
        # Inicjalizacja płaskiej listy kafelków
        self.tiles = [MapTile([x, y]) for x in range(24) for y in range(24)]
        
        # Tworzenie słownika dla szybkiego dostępu po współrzędnych
        self.tiles_dict = {}
        for tile in self.tiles:
            key = (tile.position[0], tile.position[1])
            self.tiles_dict[key] = tile
    
    def __getitem__(self, key):
        """Obsługuje dostęp przez map[x, y]"""
        if isinstance(key, tuple) and len(key) == 2:
            x, y = key
        else:
            # Jeśli dostęp przez pojedynczy argument, który jest krotką
            x, y = key[0], key[1]
            
        # Zwróć kafelek lub None, jeśli nie istnieje
        return self.tiles_dict.get((x, y))
    
    def __iter__(self):
        """Umożliwia iterację: for tile in map:"""
        return iter(self.tiles)