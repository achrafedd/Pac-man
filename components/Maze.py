from enum import Enum
from typing import Any

import arcade
from mazegenerator import MazeGenerator

from .utils import Config


class Direction(Enum):
    """Represent direction behavior.
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Maze:
    """Represent maze behavior.
    """
    def __init__(
        self,
        width: int,
        height: int,
        config: Config,
        seed: int,
        window_width: int,
        window_height: int,
    ) -> None:
        """Initialize the object.

        Args:
            width (int): Value used by the operation.
            height (int): Value used by the operation.
            config (Config): Value used by the operation.
            seed (int): Value used by the operation.
            window_width (int): Value used by the operation.
            window_height (int): Value used by the operation.
        """
        self.maze: Any = []
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
        """Perform the init gums operation.
        """
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
        """Perform the init maze operation.
        """
        maze = MazeGenerator((self.width, self.height), False)
        maze.generate(self.seed)
        self.maze = maze.maze

    @staticmethod
    def is_open(cell_value: int, direction: Direction) -> bool:
        """Perform the is open operation.

        Args:
            cell_value (int): Value used by the operation.
            direction (Direction): Value used by the operation.

        Returns:
            bool: The operation result.
        """
        return cell_value & direction.value != 0

    def get_neighbor(self, x: int, y: int) -> list[tuple[int, int]]:
        """Perform the get neighbor operation.

        Args:
            x (int): Value used by the operation.
            y (int): Value used by the operation.

        Returns:
            list[tuple[int, int]]: The operation result.
        """
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
        """Perform the grid to pixel operation.

        Args:
            col (int): Value used by the operation.
            row (int): Value used by the operation.
            tile_size (float): Value used by the operation.

        Returns:
            tuple[float, float]: The operation result.
        """
        margin_x: float = tile_size * (len(self.maze[0]) // 2)
        margin_y: float = tile_size * (len(self.maze) // 2)
        x: float = self.cx + col * tile_size - margin_x
        y: float = self.cy - row * tile_size + margin_y
        return x, y

    def draw_cell(self, row_idx: int, col_idx: int, col: int) -> None:
        """Perform the draw cell operation.

        Args:
            row_idx (int): Value used by the operation.
            col_idx (int): Value used by the operation.
            col (int): Value used by the operation.
        """
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
        """Perform the draw operation.
        """
        for row_idx, row in enumerate(self.maze):
            for col_idx, col in enumerate(row):
                self.draw_cell(row_idx, col_idx, col)
