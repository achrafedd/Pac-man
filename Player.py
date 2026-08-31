from enum import Enum
from math import sin

import arcade

from Maze import Maze


class Direction(Enum):
    RIGHT = 'right'
    LEFT = 'left'
    DOWN = 'down'
    UP = 'up'


class Player:
    def __init__(self,
                 cordinates: tuple[int, int],
                 maze: Maze,
                 direction: Direction = Direction.RIGHT,
                 size: int = 10
                 ) -> None:
        self.d: float = 1
        self.x: int = cordinates[0]
        self.y: int = cordinates[1]
        self.maze: Maze = maze
        self.direction: Direction = direction
        self.size: int = size
        self.directions: dict[str, tuple[int, int]] = {
                'right': (2, 1, 0, 30, 330),
                'down': (4, 0, 1, 300, 600),
                'left': (8, -1, 0, 210, 510),
                'up': (1, 0, -1, 120, 420)
                }

    def draw(self) -> None:
        dx, dy = self.maze.grid_to_pixel(self.x, self.y, self.maze.size)
        se: float = self.directions[self.direction.value][-2] + 20 * sin(self.d)
        ee: float = self.directions[self.direction.value][-1] - 20 * sin(self.d)
        arcade.draw_arc_filled(dx,
                               dy,
                               self.size,
                               self.size,
                               arcade.color.YELLOW,
                               se,
                               ee)

    def can_move(self, x, y, dir):
        mask, _, _, _, _ = self.directions[dir.value]
        return not self.maze.maze[y][x] & mask

    def move(self) -> None:
        mask, dx, dy, _, _ = self.directions[self.direction.value]
        if self.can_move(self.x, self.y, self.direction):
            self.x += dx
            self.y += dy
