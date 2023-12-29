from collections import Counter
import itertools
from rules import abstract_rules
from typing import Sequence

AbstractRules = abstract_rules.AbstractRules
Constraints = abstract_rules.Constraints
Directions = abstract_rules.Directions
Tile = abstract_rules.Tile
Tiles = abstract_rules.Tiles

class Rules(AbstractRules):
    def __init__(self, 
                 values: Sequence[int] = (0,1,2,3,4,5,6),
                 pow: float = 1.0):
        self._values = values
        self._pow = pow
        super().__init__()
        
    def valid_check(self, tile_value: Sequence[int]) -> bool:
        abs0 = abs(tile_value[0] - tile_value[1])
        abs1 = abs(tile_value[0] - tile_value[2])
        abs2 = abs(tile_value[1] - tile_value[3])
        abs3 = abs(tile_value[2] - tile_value[3])
        return max([abs0, abs1, abs2, abs3]) <= 1
    
    def valid_neighbor(self, tile_1: Tile, tile_2: Tile, direction: Directions) -> bool:
        """Return True if the placement of tile_1 in "direction" of tile_2 is valid."""
        tile_1 = tile_1.value
        tile_2 = tile_2.value
        if direction == 'N':
            abs0 = abs(tile_1[2] - tile_2[0])
            abs1 = abs(tile_1[3] - tile_2[1])
        if direction == 'E':
            abs0 = abs(tile_1[0] - tile_2[1])
            abs1 = abs(tile_1[2] - tile_2[3])
        if direction == 'S':
            abs0 = abs(tile_1[0] - tile_2[2])
            abs1 = abs(tile_1[1] - tile_2[3])
        if direction == 'W':
            abs0 = abs(tile_1[1] - tile_2[0])
            abs1 = abs(tile_1[3] - tile_2[2])
        return max([abs0, abs1]) <= 1
    
    def get_weight_tile(self, tile_value: Sequence[int]) -> float:
        return max(Counter(tile_value).values()) ** self._pow
        
    def create_tiles(self) -> Tiles:
        tiles = []
        iter_value = [self._values for _ in range(4)]
        for tile_value in itertools.product(*iter_value):
            if self.valid_check(tile_value):
                tile = Tile(value=tile_value,
                            weight=self.get_weight_tile(tile_value))
                tiles.append(tile)
        tiles = tuple(tiles)
        return tiles