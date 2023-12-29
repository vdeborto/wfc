from abc import ABC, abstractmethod
import dataclasses
import typing
from typing import Literal, Mapping, Sequence

@dataclasses.dataclass
class Tile:
    value: Sequence[int]
    weight: float = 1.0
    
    def __len__(self):
        return len(self.value)
    
Tiles = Sequence[Tile]
Possibilities = Sequence[int]
Constraints = Sequence[Mapping[str, Possibilities]]
Directions = Literal['N', 'E', 'S', 'W']
DIRECTIONS = typing.get_args(Directions)

class AbstractRules(ABC):
    def __init__(self) -> None:
        self.tiles = self.create_tiles()
        self.constraints = self.create_constraints()
        assert len(self.tiles) > 0, "Number of tiles must be positive"
        self.len_tile = len(self.tiles[0])
        
    def __len__(self):
        return len(self.tiles)
    
    @abstractmethod
    def create_tiles(self) -> Tiles:
        pass
    
    @abstractmethod
    def valid_neighbor(self, tile_1: Tile, tile_2: Tile, direction: Directions) -> bool:
        pass
    
    def create_constraints(self) -> Constraints:
        constraints = [{direction: None for direction in DIRECTIONS} for _ in self.tiles]
        for i, tile_1 in enumerate(self.tiles):
            for direction in DIRECTIONS:
                lst_tiles_idx = []
                for k, tile_2 in enumerate(self.tiles):
                    if self.valid_neighbor(tile_1, tile_2, direction):
                        lst_tiles_idx.append(k)
                    constraints[i][direction] = set(lst_tiles_idx)
        return constraints