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
                 ) -> None:
        self.dir: int = 1
        self.d: float = 1
        self.x: int = cordinates[0]
        self.y: int = cordinates[1]
        self.maze: Maze = maze
        self.direction: Direction = direction
        self.next_direction: Direction = direction
        self.size: int = maze.size // 2
        self.speed: int = 5
        self.score: int = 0
        self.directions: dict[str, tuple[int, int, int, int, int]] = {
                'right': (2, 1, 0, 30, 330),
                'down': (4, 0, 1, 300, 600),
                'left': (8, -1, 0, 210, 510),
                'up': (1, 0, -1, 120, 420)
                }
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(self.x, self.y, maze.size)
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def draw(self) -> None:
        if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
            self.score += self.maze.gums[self.y][self.x]
            self.maze.gums[self.y][self.x] = 0
        se: float = self.directions[self.direction.value][3] + 20 * sin(self.d)
        ee: float = self.directions[self.direction.value][4] - 20 * sin(self.d)
        arcade.draw_arc_filled(self.pixel_x,
                               self.pixel_y,
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
        if  self.can_move(self.x, self.y, self.direction):
            self.x += dx
            self.y += dy
            self.target_x, self.target_y = self.maze.grid_to_pixel(self.x, self.y, self.maze.size)

    def update(self, delta_time: float) -> None:
        if self.next_direction != self.direction and self.can_move(self.x, self.y, self.next_direction):
            self.direction = self.next_direction

        if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
            self.move()

        step = self.speed * self.maze.size * delta_time
        dx = self.target_x - self.pixel_x
        dy = self.target_y - self.pixel_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance <= step or distance == 0:
            self.pixel_x, self.pixel_y = self.target_x, self.target_y
        else:
            self.pixel_x += step * dx / distance
            self.pixel_y += step * dy / distance

