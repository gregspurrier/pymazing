from pymazing.board import Board

class SquareBoard(Board):
    """A Board with square tiles."""

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

    def fill(self, num_rows, num_cols):
        for r in range(num_rows):
            for c in range(num_cols):
                self.tiles.add((r, c))

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

    @staticmethod
    def board_size(max_y, max_x):
        """Return the maximum board size as (rows, columns) for the given
        screen size.
        """
        rows = (max_y - 1) // 2
        cols = (max_x - 1) // 3
        return rows, cols
