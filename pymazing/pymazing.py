import curses

from board import Board

def play(scr):
    # Create the largest board that will fit in the window.
    y, x = scr.getmaxyx()
    rows = (y - 1) // 2
    cols = (x - 1) // 3
    b = Board(rows, cols)

    scr.clear()
    b.paint(scr)
    scr.move(1, 1)
    scr.refresh()
    scr.getkey()

curses.wrapper(play)
