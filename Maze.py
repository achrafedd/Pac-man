from enum import Enum

import arcade
from mazegenerator import MazeGenerator

from utils import Config


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        config: Config,
        seed: int,
        window_width: int,
        window_height: int,
    ) -> None:
        self.maze: list[list[int]] = []
        self.config: Config = config
        self.gums: list[list[int]]
        self.width: int = width
        self.height: int = height
        self.seed: int = seed
        self.cx: int = window_width // 2
        self.cy: int = window_height // 2 - 80
        self.init_maze()
        self.init_gums()
        self.size: float = min(
            (window_width - 100) / width, (window_height - 300) / height
        )

    def init_gums(self) -> None:
        self.gums = [[0] * self.width for _ in range(self.height)]
        for r_idx, row in enumerate(self.maze):
            for c_idx, col in enumerate(row):
                if r_idx == 0 and c_idx == 0:
                    self.gums[0][0] = self.config.points_per_super_pacgum
                elif r_idx == 0 and c_idx == self.width - 1:
                    self.gums[r_idx][c_idx] = (
                        self.config.points_per_super_pacgum
                    )
                elif r_idx == self.height - 1 and c_idx == 0:
                    self.gums[r_idx][c_idx] = (
                        self.config.points_per_super_pacgum
                    )
                elif r_idx == self.height - 1 and c_idx == self.width - 1:
                    self.gums[r_idx][c_idx] = (
                        self.config.points_per_super_pacgum
                    )
                elif col == 15:
                    self.gums[r_idx][c_idx] = 0
                else:
                    self.gums[r_idx][c_idx] = self.config.points_per_pacgum

    def init_maze(self) -> None:
        maze = MazeGenerator((self.width, self.height), False)
        maze.generate(self.seed)
        self.maze = maze.maze

    @staticmethod
    def is_open(cell_value: int, direction: Direction) -> bool:
        return cell_value & direction.value != 0

    def get_neighbor(self, x: int, y: int) -> list[tuple[int, int]]:
        cell: int = self.maze[y][x]
        neighbors = []
        if not cell >> 0 & 1 and y > 0:
            neighbors.append((y - 1, x))
        if not cell >> 1 & 1 and x < self.width - 1:
            neighbors.append((y, x + 1))
        if not cell >> 2 & 1 and y < self.height - 1:
            neighbors.append((y + 1, x))
        if not cell >> 3 & 1 and x > 0:
            neighbors.append((y, x - 1))
        return neighbors

    def grid_to_pixel(
        self, col: int, row: int, tile_size: float
    ) -> tuple[float, float]:
        margin_x: float = tile_size * (len(self.maze[0]) // 2)
        margin_y: float = tile_size * (len(self.maze) // 2)
        x: float = self.cx + col * tile_size - margin_x
        y: float = self.cy - row * tile_size + margin_y
        return x, y

    def draw_cell(self, row_idx: int, col_idx: int, col: int):
        half = self.size // 2
        x, y = self.grid_to_pixel(col_idx, row_idx, self.size)
        rect = arcade.XYWH(x, y, self.size, self.size)

        # Draw 42 rect
        if col == 15:
            arcade.draw_rect_filled(rect, (255, 255, 255))
        else:
            arcade.draw_rect_filled(rect, (0, 0, 0))

        # Draw Gums
        if self.gums[row_idx][col_idx] == self.config.points_per_pacgum:
            arcade.draw_circle_filled(
                x, y, 3, arcade.color.WHITE, tilt_angle=100
            )
        elif (
            self.gums[row_idx][col_idx] == self.config.points_per_super_pacgum
        ):
            arcade.draw_circle_filled(
                x, y, 10, arcade.color.WHITE, tilt_angle=100
            )

        # Draw the Cell
        if self.is_open(col, Direction.NORTH):
            arcade.draw_line(
                x - half, y + half, x + half, y + half, arcade.color.BLUE, 3
            )
        if self.is_open(col, Direction.EAST):
            arcade.draw_line(
                x + half, y - half, x + half, y + half, arcade.color.BLUE, 3
            )
        if self.is_open(col, Direction.SOUTH):
            arcade.draw_line(
                x - half, y - half, x + half, y - half, arcade.color.BLUE, 3
            )
        if self.is_open(col, Direction.WEST):
            arcade.draw_line(
                x - half, y + half, x - half, y - half, arcade.color.BLUE, 3
            )

    def draw(self) -> None:
        for row_idx, row in enumerate(self.maze):
            for col_idx, col in enumerate(row):
                self.draw_cell(row_idx, col_idx, col)
