import curses
from utils import draw_grid_diff, is_cell_living, toggle_cells, init_curses
import time
import random

class Game:
    TICK_SPEED = 0.06

    def __init__(self, height: int, width: int, population_rate: float):
        self.height = height - 1
        self.width = width - 1
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.populate(population_rate)

    def populate(self, population_rate: float):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = 1 if random.random() < population_rate else 0

    def update(self):
        updated = [row[:] for row in self.grid]
        for row in range(self.height):
            for col in range(self.width):
                updated[row][col] = is_cell_living(self.grid, row, col, self.height, self.width)
        self.grid = updated
        return updated

    def next_evolution(self, stdscr):
        old_grid = self.grid
        new_grid = self.update()
        draw_grid_diff(stdscr, old_grid, new_grid, self.height, self.width)
        stdscr.refresh()

    def update(self):
        updated = [row[:] for row in self.grid]
        for row in range(self.height):
            for col in range(self.width):
                updated[row][col] = is_cell_living(self.grid, row, col, self.height, self.width)
        self.grid = updated
        return updated

    def __str__(self):
        return "\n".join(
                    " ".join(str(j) for j in i) for i in self.grid
                )

def main(stdscr):
    # Create game
    h, w = stdscr.getmaxyx()
    population_rate = 0.15
    game = Game(h, w, population_rate=0.15)
    init_curses(stdscr)

    while True:
        # Look for cursor events
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            if 0 <= my < game.height and 0 <= mx < game.width:
                toggle_cells(game.grid, game.height, game.width, my, mx, rand_shape=True)
        elif key in (ord('q'), 27): # q or ESCAPE key
            return
        elif key == curses.ERR:
            pass

        game.next_evolution(stdscr)
        time.sleep(game.TICK_SPEED)