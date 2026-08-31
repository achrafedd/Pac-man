from enum import Enum

import arcade
from mazegenerator import MazeGenerator


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Maze:
    def __init__(self, width: int,
                 height: int,
                 seed: int,
                 window_width: int,
                 window_height: int) -> None:
        self.maze: list[list[int]] = []
        self.width: int = width
        self.height: int = height
        self.seed: int = seed
        self.cx: int = window_width // 2
        self.cy: int = window_height // 2
        self.init_maze()
        self.size: float = min(
                        window_width // len(self.maze),
                        window_height // len(self.maze[0]))

    def init_maze(self) -> None:
        maze = MazeGenerator((self.width, self.height), False)
        maze.generate(self.seed)
        self.maze = maze.maze

    @staticmethod
    def is_open(cell_value: int, direction: Direction) -> bool:
        return cell_value & direction.value != 0

    def grid_to_pixel(self, col, row, tile_size) -> tuple[int, int]:
        margin_x = tile_size * (len(self.maze[0]) // 2)
        margin_y = tile_size * (len(self.maze) // 2)
        x = self.cx + col * tile_size - margin_x
        y = self.cy - row * tile_size + margin_y
        return x, y

    def draw_cell(self, row_idx: int, col_idx: int, col: int):
        half = self.size // 2
        x, y = self.grid_to_pixel(col_idx, row_idx, self.size)
        arcade.draw_circle_filled(x, y, 3, arcade.color.WHITE)
        if self.is_open(col, Direction.NORTH):
            arcade.draw_line(x - half, y + half, x + half, y + half, arcade.color.BLUE, 3)
        if self.is_open(col, Direction.EAST):
            arcade.draw_line(x + half, y - half, x + half, y + half, arcade.color.BLUE, 3)
        if self.is_open(col, Direction.SOUTH):
            arcade.draw_line(x - half, y - half, x + half, y - half, arcade.color.BLUE, 3)
        if self.is_open(col, Direction.WEST):
            arcade.draw_line(x - half, y + half, x - half, y - half, arcade.color.BLUE, 3)

    def draw(self, window_width: float, window_height: float) -> None:
        for row_idx, row in enumerate(self.maze):
            for col_idx, col in enumerate(row):
                self.draw_cell(row_idx, col_idx, col)
