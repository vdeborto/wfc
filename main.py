from absl import app
from absl import flags
import importlib
import math
import matplotlib.pyplot as plt
import numpy as np
import random
from rules import abstract_rules
from typing import Optional, Sequence

FLAGS = flags.FLAGS
flags.DEFINE_string('rule_type', 'terrain', 'Set of rules to build the map')
flags.DEFINE_integer('height', 4, 'Height of the map')
flags.DEFINE_integer('width', 4, 'Width of the map')
flags.DEFINE_integer('max_it', int(1e9), 'Maximum number of iterations in the generation')
flags.DEFINE_integer('stride_eval', int(1e3), 'Stride for the evaluation in the generation')

DIRECTIONS = abstract_rules.DIRECTIONS
Possibilities = abstract_rules.Possibilities
Rules = abstract_rules.AbstractRules
EntropyTiling = Sequence[Sequence[Possibilities]]
TileMap = np.ndarray[float]
Map = np.ndarray[float]

class Tiling:
    def __init__(self, 
                 rules: Rules,
                 height: int,
                 width: int,
                 max_it: int,
                 stride_eval: int):
        self._rules = rules
        self._tiles = rules.tiles
        self._constraints = rules.constraints
        self._len_tile = rules.len_tile
        self._height = height
        self._width = width
        self._max_it = max_it
        self._stride_eval = stride_eval
        self._entropy_tiling = self._init_tiling()
        self._wavefunction_collapse()
        
    def _init_tiling(self) -> EntropyTiling:
        return [[tuple(range(len(self._rules))) for _ in range(self._width)] for _ in range(self._height)]

    def _get_min_entropy_idx(self) -> tuple[Sequence[int], int]:
        entropy_tiling = self._entropy_tiling
        min_entropy_idx, m = [], float("inf")
        for i in range(self._height):
            for j in range(self._width):
                if len(entropy_tiling[i][j]) == 1:
                    continue
                if len(entropy_tiling[i][j]) == m:
                    min_entropy_idx.append([i,j])
                if len(entropy_tiling[i][j]) < m:
                    min_entropy_idx = [[i,j]]
                    m = len(entropy_tiling[i][j])
        return min_entropy_idx, m

    def _get_weights(self, idx_lst: Possibilities) -> Sequence[float]:
        weights = []
        for idx in idx_lst:
            weights.append(self._tiles[idx].weight)
        return weights

    def _collapse(self, min_entropy_idx: Sequence[int]) -> tuple[int, int]:
        i, j = random.choice(min_entropy_idx)
        possibilities = self._entropy_tiling[i][j]
        weights = self._get_weights(possibilities)
        value = random.choices(possibilities, weights=weights)
        self._entropy_tiling[i][j] = value
        return (i, j)

    def _update_tile_array(self, idx: tuple[int, int]):
        stack = [idx]
        while stack:
            i, j = stack.pop()
            possibilities_1 = self._entropy_tiling[i][j]
            for d, (i_new, j_new) in zip(DIRECTIONS, [(i+1, j), (i, j-1), (i-1, j), (i, j+1)]):
                if 0 <= i_new < self._height and 0 <= j_new < self._width:
                    possibilities_2 = self._entropy_tiling[i_new][j_new]
                    possibilities = set()
                    for tile_idx_1 in possibilities_1:
                        possibilities = possibilities.union(self._constraints[tile_idx_1][d])
                    possibilities_2_set = set(possibilities_2)
                    new_possibilities_2 = tuple(possibilities_2_set.intersection(possibilities))
                    self._entropy_tiling[i_new][j_new] = new_possibilities_2
                    if len(new_possibilities_2) < len(possibilities_2):
                        stack.append((i_new, j_new))

    def _wavefunction_collapse(self):
        min_entropy_idx, m = self._get_min_entropy_idx()
        k = 0
        while m < float("inf"):
            idx = self._collapse(min_entropy_idx)
            self._update_tile_array(idx)
            min_entropy_idx, m = self._get_min_entropy_idx()
            k += 1
            assert k < self._max_it, f"Maximum iteration is {self._max_it}"
            if k % self._stride_eval == 0:
                save_map(self.map_generator(), k=k)
                
    def _superposition(self, possibilities: Possibilities) -> TileMap:
        n_possibilities = len(possibilities)
        len_tile_reshape = int(math.sqrt(self._len_tile))
        tile_map = np.zeros((len_tile_reshape, len_tile_reshape))
        for tile_idx in possibilities:
            tile_value = self._tiles[tile_idx].value
            tile_map += np.reshape(tile_value,
                                   (len_tile_reshape, len_tile_reshape))
        return tile_map / n_possibilities

    def map_generator(self) -> Map:
        entropy_tiling = self._entropy_tiling
        len_tile_reshape = int(math.sqrt(self._len_tile))
        map = np.zeros((len_tile_reshape * self._height, 
                        len_tile_reshape * self._width))
        for row in range(len(entropy_tiling)):
            for col in range(len(entropy_tiling[0])):
                tile_map = self._superposition(entropy_tiling[row][col])
                row_min = len_tile_reshape * row
                row_max = row_min + len_tile_reshape
                col_min = len_tile_reshape * col
                col_max = col_min + len_tile_reshape
                map[row_min:row_max, :][:, col_min:col_max] = tile_map
        return map

def save_map(map: Map, k: Optional[int]=None):
    filename = f'map_it{k}.png' if k else 'map.png'
    plt.imsave(filename, map, cmap='gray')

def main(argv):
    del argv
    main_rules = importlib.import_module(f'rules.{FLAGS.rule_type}')
    rules = main_rules.Rules()
    tiling = Tiling(rules=rules,
                    height=FLAGS.height,
                    width=FLAGS.width,
                    max_it=FLAGS.max_it,
                    stride_eval=FLAGS.stride_eval)
    map = tiling.map_generator()
    save_map(map)

if __name__ == '__main__':
    app.run(main)