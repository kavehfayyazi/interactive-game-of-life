from curses import wrapper, textpad
import curses
import time
import random

class Game:
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

    def __str__(self):
        return "\n".join(
                    " ".join(str(j) for j in i) for i in self.grid
                )

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

def draw_game(window: curses.window, game: Game):
    for row in range(game.height):
        for col in range(game.width):
            if game.grid[row][col]:
                window.addstr(row, col, ' ', curses.color_pair(1))
            else:
                window.addstr(row, col, ' ', curses.color_pair(2))

def main(stdscr):
    # Create game
    (height, width) = stdscr.getmaxyx()
    population_rate = 0.15
    game = Game(height, width, population_rate)
    
    # Hide cursor
    curses.curs_set(0)

    # Enable color functionality
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE) # color_number of 1 for white
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK) # color_number of 2 for black

    # Infinite game loop
    while True:
        stdscr.refresh()
        draw_game(stdscr, game)
        game.update()
        time.sleep(0.1)

if __name__ == '__main__':
    wrapper(main)