'''
	Dijkstraalgorithm.py

	Copyright (c) PAUL MICKY D COSTA
	Licensed under the MIT license: https://opensource.org/license/mit
'''

import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Path Finding Algorithm")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Vertex:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.distance = float("inf")  # Distance from start node
        self.previous = None  # Previous node in the shortest path

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        self.distance = float("inf")
        self.previous = None

    def make_closed(self):
        self.color = RED

    def make_start(self):
        self.color = ORANGE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    # This is the critical update
    def __lt__(self, other):
        return self.distance < other.distance

# Dijkstra Algorithm
def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    start.distance = 0
    visited = set()

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        visited.add(current)

        if current == end:
            reconstruct_path(current, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                new_dist = current.distance + 1
                if new_dist < neighbor.distance:
                    neighbor.distance = new_dist
                    neighbor.previous = current
                    open_set.put((neighbor.distance, neighbor))
                    neighbor.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False

# Reconstruct path from the end node to the start node
def reconstruct_path(current, draw):
    while current.previous:
        current = current.previous
        current.make_path()
        draw()

# Create grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            vertex = Vertex(i, j, gap, rows)
            grid[i].append(vertex)
    return grid

# Draw grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Draw everything
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for vertex in row:
            vertex.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Get clicked position
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# Main function with default start, end, and barriers
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    # Default positions for start, end, and barriers
    start = grid[10][10]
    end = grid[40][40]

    # Add some barriers (you can customize these positions)
    grid[20][20].make_barrier()
    grid[20][21].make_barrier()
    grid[21][20].make_barrier()
    grid[21][21].make_barrier()

    start.make_start()
    end.make_end()

    # Run Dijkstra algorithm directly
    for row in grid:
        for vertex in row:
            vertex.update_neighbors(grid)
    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

    # Wait for the user to close the window after pathfinding
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()

main(WIN, WIDTH)
