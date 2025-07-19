import curses
import random
from tables import PATTERNS_OFFSET_MAPPINGS

def init_curses(stdscr):
    # Cursor
    curses.curs_set(0)
    curses.mouseinterval(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    stdscr.nodelay(True)

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE) # color_number of 1 for white
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK) # color_number of 2 for black

def toggle_cells(grid, height, width, y, x, rand_shape = False):
    if rand_shape:
        shape = random.choice(list(PATTERNS_OFFSET_MAPPINGS.values()))
        for (y_offset, x_offset) in shape:
            row = (y + y_offset + height) % height
            col = (x + x_offset + width) % width
            grid[row][col] ^= 1
    else:
        grid[y][x] ^= 1


def draw_grid_diff(window: curses.window, old_grid, new_grid, height, width):
    for row in range(height):
        for col in range(width):
            if old_grid[row][col] != new_grid[row][col]:
                color = curses.color_pair(1) if new_grid[row][col] else curses.color_pair(2)
                window.addstr(row, col, ' ', color)
                
def is_cell_living(grid: list[list[int]], row: int, col: int, height: int, width: int) -> bool:
    # Ensure no index out of bound, with wraparound.
    neighbors_y = [(row - 1 + height) % height, row, (row + 1) % height]
    neighbors_x = [(col - 1 + width) % width, col, (col + 1) % width]
    
    neighbors_alive = 0
    for y in neighbors_y:
        for x in neighbors_x:
            if not (y == row and x == col): neighbors_alive += grid[y][x]
    if grid[row][col]:  return neighbors_alive in [2,3]
    else:               return neighbors_alive == 3
