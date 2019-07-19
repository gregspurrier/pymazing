import unittest

from hypothesis import given
from hypothesis.strategies import integers

from pymazing.square_board import SquareBoard

class TestSquareBoardCreation(unittest.TestCase):
    @given(integers(2, 5), integers(2, 5), integers())
    def test_tiles_fill_board(self, rows, cols, seed):
        b = SquareBoard(rows, cols, seed)
        self.assertEqual(len(b.tiles), rows * cols)
        for r in range(rows):
            for c in range(cols):
                self.assertTrue((r, c) in b.tiles)

    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_visit_all_tiles(self, rows, cols, seed):
        b = SquareBoard(rows, cols, seed)
        self.assertEqual(set(b.tile_exits.keys()), b.tiles)

    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_are_reflexive(self, rows, cols, seed):
        inverted_dirs = {'n': 's',
                         'w': 'e',
                         'e': 'w',
                         's': 'n'}
        b = SquareBoard(rows, cols, seed)
        for tile, exits in b.tile_exits.items():
            for d, neighbor in exits.items():
                self.assertEqual(b.tile_exits[neighbor][inverted_dirs[d]],
                                 tile)

    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_lead_to_adjacent_tiles(self, rows, cols, seed):
        b = SquareBoard(rows, cols, seed)
        for tile, exits in b.tile_exits.items():
            for d, dest in exits.items():
                self.assertEqual(dest, self.adjacent_tile(tile, d))


    @given(integers(2, 5), integers(2, 5), integers())
    def test_tile_exits_encode_a_spanning_tree(self, rows, cols, seed):
        def make_edge(tile1, tile2):
            if tile1 < tile2:
                return (tile1, tile2)
            else:
                return (tile2, tile1)

        b = SquareBoard(rows, cols, seed)
        edges = set()
        for tile, exits in b.tile_exits.items():
            for neighbor in exits.values():
                edges.add(make_edge(tile, neighbor))
        # A spanning tree has |V|-1 edges and covers V.
        self.assertEqual(len(edges), len(b.tiles) - 1)
        visited = set()
        for (tile1, tile2) in edges:
            self.assertNotEqual(tile1, tile2)
            visited.add(tile1)
            visited.add(tile2)
        self.assertEqual(visited, b.tiles)

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

class ScreenBuffer:
    """Minimal implementation of curses.Window that accumulates characters in a
    screen buffer."""
    def __init__(self, maxy, maxx):
        self.maxx = maxx
        self.maxy = maxy
        self.buffer = [[' '] * maxx for _ in range(maxy)]

    def addch(self, y, x, ch):
        if not 0 <= y < self.maxy:
            raise ValueError("y out of bounds: " + str(y))
        if not 0 <= x <= self.maxx:
            raise ValueError("x out of bounds: " + str(x))
        self.buffer[y][x] = ch

    def addstr(self, y, x, str):
        for i, ch in enumerate(str):
            self.addch(y, x + i, ch)

class TestSquareBoardPainting(unittest.TestCase):
    @given(integers(2, 5), integers(2, 5), integers())
    def test_painting(self, rows, cols, seed):
        b = SquareBoard(rows, cols, seed)
        scr = ScreenBuffer(rows * 2 + 1, cols * 3 + 1)
        b.paint(scr)
        for tile in b.tiles:
            r, c = tile
            x = c * 3
            y = r * 2
            if 'n' in b.tile_exits[tile]:
                self.assertEqual(scr.buffer[y][x:x + 4], list('+  +'))
            else:
                self.assertEqual(scr.buffer[y][x:x + 4], list('+--+'))
            if 'w' in b.tile_exits[tile]:
                self.assertEqual(scr.buffer[y + 1][x:x + 3], list('   '))
            else:
                self.assertEqual(scr.buffer[y + 1][x:x + 3], list('|  '))
            if 'e' in b.tile_exits[tile]:
                self.assertEqual(scr.buffer[y + 1][x + 3], ' ')
            else:
                self.assertEqual(scr.buffer[y + 1][x + 3], '|')
            if 's' in b.tile_exits[tile]:
                self.assertEqual(scr.buffer[y + 2][x:x + 4], list('+  +'))
            else:
                self.assertEqual(scr.buffer[y + 2][x:x + 4], list('+--+'))
