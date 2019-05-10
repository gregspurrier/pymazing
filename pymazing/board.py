import random

class Board:
    """Board represents a two-dimensional playing surface upon which tiles are
    placed to form the cells of a maze."""

    # Offsets to neighboring tiles indexed by movement direction.
    _offsets = {
        'n': (-1, 0),
        'w': (0, -1),
        'e': (0, 1),
        's': (1, 0)
    }

    _inverted_dirs = {
        'n': 's',
        'w': 'e',
        'e': 'w',
        's': 'n'
    }

    def __init__(self, num_rows, num_cols, rand_seed=None):
        self.rand = random.Random(rand_seed)
        self.tiles = set()
        self.fill(num_rows, num_cols)
        self.tile_exits = self.blaze()

    def blaze(self):
        """Find a random path visiting all tiles in self.tiles.

        The result is a tile -> direction -> tile dictionary that, for each
        tile, gives the directions via which the tile can be exited and the
        tile that is reached by travelling in each of those directions."""
        visited = set()
        tile_exits = dict((tile, {}) for tile in self.tiles)

        def visit(tile):
            # Randomized depth-first search of self.tiles.
            visited.add(tile)
            adj = self.adjacencies(tile, self.tiles)
            self.rand.shuffle(adj)
            for d, t in adj:
                if t not in visited:
                    tile_exits[tile][d] = t
                    tile_exits[t][self._inverted_dirs[d]] = tile
                    visit(t)

        visit(next(iter(self.tiles)))
        return tile_exits

    def paint(self, scr):
        for tile in self.tiles:
            self.paint_tile(tile, scr)

    def paint_tile(self, tile, scr):
        r, c = tile
        x = c * 3
        y = r * 2
        scr.addch(y, x, '+')
        scr.addch(y, x + 3, '+')
        scr.addch(y + 2, x, '+')
        scr.addch(y + 2, x + 3, '+')
        if 'n' not in self.tile_exits[tile]:
            scr.addstr(y, x + 1, '--')
        if 'w' not in self.tile_exits[tile]:
            scr.addch(y + 1, x, '|')
        if 'e' not in self.tile_exits[tile]:
            scr.addch(y + 1, x + 3, '|')
        if 's' not in self.tile_exits[tile]:
            scr.addstr(y + 2, x + 1, '--')

    def adjacencies(self, tile, tile_set):
        """Return the (direction, tile) pairs corresponding to the tiles that
        are adjacent to tile in the provided tile_set as a list."""
        r, c = tile
        ns = []
        for d, (dr, dc) in self._offsets.items():
            other = (r + dr, c + dc)
            if other in tile_set:
                ns.append((d, other))
        return ns

    def fill(self, num_rows, num_cols):
        for r in range(num_rows):
            for c in range(num_cols):
                self.tiles.add((r, c))
