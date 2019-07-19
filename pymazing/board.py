import random

class Board:
    """Board represents a two-dimensional playing surface upon which tiles are
    placed to form the cells of a maze."""

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

    def fill(self, num_rows, num_cols):
        for r in range(num_rows):
            for c in range(num_cols):
                self.tiles.add((r, c))
