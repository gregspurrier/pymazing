import curses
import sys

from pymazing.hex_board import HexBoard
from pymazing.square_board import SquareBoard

def run():
    def play(scr):
        board_cls = SquareBoard
        if len(sys.argv) > 1:
            board_type = sys.argv[1]
            if board_type == 'hexagon':
                board_cls = HexBoard
            elif board_type == 'square':
                board_cls = SquareBoard
            else:
                print('Unrecognized board type:', board_type)
                sys.exit(1)

        # Create the largest board that will fit in the window.
        max_y, max_x = scr.getmaxyx()
        rows, cols = board_cls.board_size(max_y, max_x)
        b = board_cls(rows, cols)

        scr.clear()
        b.paint(scr)
        scr.move(1, 1)
        scr.refresh()
        scr.getkey()

    curses.wrapper(play)
