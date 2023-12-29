from collections import Counter
from rules import abstract_rules
from typing import Sequence

AbstractRules = abstract_rules.AbstractRules
Constraints = abstract_rules.Constraints
Directions = abstract_rules.Directions
Tile = abstract_rules.Tile
Tiles = abstract_rules.Tiles

class Rules(AbstractRules):
    def __init__(self, 
                 values: Sequence[int] = (0,1),
                 pow: float = 1.0):
        self._values = values
        self._pow = pow
        super().__init__()
    
    def valid_neighbor(self, tile_1: Tile, tile_2: Tile, direction: Directions) -> bool:
        """Return True if the placement of tile_1 in "direction" of tile_2 is valid."""
        tile_1 = tile_1.value
        tile_2 = tile_2.value
        if direction == 'N':
            abs0 = abs(tile_1[6] - tile_2[0])
            abs1 = abs(tile_1[7] - tile_2[1])
            abs2 = abs(tile_1[8] - tile_2[2])
        if direction == 'E':
            abs0 = abs(tile_1[0] - tile_2[2])
            abs1 = abs(tile_1[3] - tile_2[5])
            abs2 = abs(tile_1[6] - tile_2[8])
        if direction == 'S':
            abs0 = abs(tile_1[0] - tile_2[6])
            abs1 = abs(tile_1[1] - tile_2[7])
            abs2 = abs(tile_1[2] - tile_2[8])
        if direction == 'W':
            abs0 = abs(tile_1[2] - tile_2[0])
            abs1 = abs(tile_1[5] - tile_2[3])
            abs2 = abs(tile_1[8] - tile_2[6])
        return max([abs0, abs1, abs2]) == 0
    
    def get_weight_tile(self, tile_value: Sequence[int]) -> float:
        del tile_value
        return 1.0
        
    def create_tiles(self) -> Tiles:
        tiles_values = [[0,1,0,1,1,0,0,0,0],
                        [0,1,0,0,1,1,0,0,0],
                        [0,0,0,0,1,1,0,1,0],
                        [0,0,0,1,1,0,0,1,0],
                        [0,1,0,0,1,0,0,1,0],
                        [0,0,0,1,1,1,0,0,0],
                        [0,1,0,1,1,1,0,1,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,1,1,1,0,1,0],
                        [0,1,0,0,1,1,0,1,0],
                        [0,1,0,1,1,1,0,0,0],
                        [0,1,0,1,1,0,0,1,0],
                        [0,1,0,0,1,0,0,0,0],
                        [0,0,0,0,1,0,0,1,0],
                        [0,0,0,1,1,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0]]
        tiles = [Tile(value=tile_value, weight=self.get_weight_tile(tile_value)) for tile_value in tiles_values]
        return tiles
