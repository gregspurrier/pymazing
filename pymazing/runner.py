import curses

from pymazing.square_board import SquareBoard

def run():
    def play(scr):
        # Create the largest board that will fit in the window.
        y, x = scr.getmaxyx()
        rows = (y - 1) // 2
        cols = (x - 1) // 3
        b = SquareBoard(rows, cols)

        scr.clear()
        b.paint(scr)
        scr.move(1, 1)
        scr.refresh()
        scr.getkey()

    curses.wrapper(play)
