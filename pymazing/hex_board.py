from pymazing.board import Board

class HexBoard(Board):
    """A Board with hexagonal tiles."""

    #             Tile (row, col)        Screen (y, x) Origin
    #  _   _   _  ---------------------|---------------------
    # / \_/ \_/ \ (0, 0) (0, 2) (0, 4) | (0, 0) (0, 4) (0, 8)
    # \_/ \_/ \_/ (1, 1) (1, 3)        | (1, 2) (1, 6)
    # / \_/ \_/ \ (2, 0) (2, 2) (2, 4) | (2, 0) (2, 4) (2, 8)
    # \_/ \_/ \_/ (3, 1) (3, 3)        | (3, 2) (3, 6)
    #   \_/ \_/

    # Cols | Characters  |   Rows | Lines
    # 1      3               1      3
    # 2      4               2      4
    # 3      7               3      5
    # 4      9               4      6


    # Offsets to neighboring tiles indexed by movement direction.
    _offsets = {
        'n': (-2, 0),
        'nw': (-1, -1),
        'ne': (-1, 1),
        'sw': (1, -1),
        'se': (1, 1),
        's': (2, 0)
    }

    _inverted_dirs = {
        'n': 's',
        'nw': 'se',
        'ne': 'sw',
        'sw': 'ne',
        'se': 'nw',
        's': 'n'
    }

    def fill(self, num_rows, num_cols):
        for r in range(0, num_rows, 2):
            for c in range(0, num_cols, 2):
                self.tiles.add((r, c))
        for r in range(1, num_rows, 2):
            for c in range(1, num_cols, 2):
                self.tiles.add((r, c))

    def paint_tile(self, tile, scr):
        r, c = tile
        y = r
        x = c * 2

        if 'n' not in self.tile_exits[tile]:
            scr.addch(y, x + 1, '_')
        if 'nw' not in self.tile_exits[tile]:
            scr.addch(y + 1, x, '/')
        if 'ne' not in self.tile_exits[tile]:
            scr.addch(y + 1, x + 2, '\\')
        if 'sw' not in self.tile_exits[tile]:
            scr.addch(y + 2, x, '\\')
        if 'se' not in self.tile_exits[tile]:
            scr.addch(y + 2, x + 2, '/')
        if 's' not in self.tile_exits[tile]:
            scr.addch(y + 2, x + 1, '_')

    @staticmethod
    def board_size(max_y, max_x):
        """Return the maximum board size as (rows, columns) for the given
        screen size.
        """
        rows = max_y - 3
        cols = (max_x - 1) // 2
        return rows, cols
