import unittest
from pymazing.board import Board

from hypothesis import given
from hypothesis.strategies import integers

class TestBlaze(unittest.TestCase):
    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_visit_all_tiles(self, rows, cols, seed):
        tile_set = self.make_tile_set(rows, cols)
        b = Board(rand_seed=seed)
        tile_exits = b.blaze(tile_set)
        self.assertEqual(set(tile_exits.keys()), tile_set)

    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_are_reflexive(self, rows, cols, seed):
        inverted_dirs = {'n': 's',
                         'w': 'e',
                         'e': 'w',
                         's': 'n'}
        tile_set = self.make_tile_set(rows, cols)
        b = Board(rand_seed=seed)
        tile_exits = b.blaze(tile_set)
        for tile, exits in tile_exits.items():
            for d, neighbor in exits.items():
                self.assertEqual(tile_exits[neighbor][inverted_dirs[d]], tile)

    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_lead_to_adjacent_tiles(self, rows, cols, seed):
        tile_set = self.make_tile_set(rows, cols)
        b = Board(rand_seed=seed)
        tile_exits = b.blaze(tile_set)
        for tile, exits in tile_exits.items():
            for d, dest in exits.items():
                self.assertEqual(dest, self.adjacent_tile(tile, d))


    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_encode_a_spanning_tree(self, rows, cols, seed):
        def make_edge(tile1, tile2):
            if tile1 < tile2:
                return (tile1, tile2)
            else:
                return (tile2, tile1)

        tile_set = self.make_tile_set(rows, cols)
        b = Board(rand_seed=seed)
        tile_exits = b.blaze(tile_set)
        edges = set()
        for tile, exits in tile_exits.items():
            for neighbor in exits.values():
                edges.add(make_edge(tile, neighbor))
        # A spanning tree has |V|-1 edges and covers V.
        self.assertEqual(len(edges), len(tile_set) - 1)
        visited = set()
        for (tile1, tile2) in edges:
            self.assertNotEqual(tile1, tile2)
            visited.add(tile1)
            visited.add(tile2)
        self.assertEqual(visited, tile_set)

    def make_tile_set(self, rows, cols):
        return set((r, c) for r in range(rows)
                          for c in range(cols))

    def adjacent_tile(self, tile, d):
        """Return the tile adjacent to tile in direction d."""
        row, col = tile
        if d == 'n':
            return (row - 1, col)
        elif d == 'w':
            return (row, col - 1)
        elif d == 'e':
            return (row, col + 1)
        elif d == 's':
            return (row + 1, col)

