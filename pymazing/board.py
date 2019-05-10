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

    def __init__(self, rand_seed=None):
        self.rand = random.Random(rand_seed)
        pass

    def blaze(self, tile_set):
        """Find a random path visiting all tiles in tile_set.

        The result is a tile -> direction -> tile dictionary that, for each
        tile, gives the directions via which the tile can be exited and the
        tile that is reached by travelling in each of those directions."""
        visited = set()
        tile_exits = dict((tile, {}) for tile in tile_set)

        def visit(tile):
            # Randomized depth-first search of tile_set.
            visited.add(tile)
            adj = self.adjacencies(tile, tile_set)
            self.rand.shuffle(adj)
            for d, t in adj:
                if t not in visited:
                    tile_exits[tile][d] = t
                    tile_exits[t][self._inverted_dirs[d]] = tile
                    visit(t)

        visit(next(iter(tile_set)))
        return tile_exits

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
