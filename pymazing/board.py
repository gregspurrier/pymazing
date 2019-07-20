import random

class Board:
    """Board represents a two-dimensional playing surface upon which tiles are
    placed to form the cells of a maze."""

    def __init__(self, num_rows, num_cols, rand_seed=None):
        self.rand = random.Random(rand_seed)
        self.tiles = set()
        self.fill(num_rows, num_cols)
        self.tile_exits = self.blaze()
        # self.tile_exits = {tile: {} for tile in self.tiles}

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
