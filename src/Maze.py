import arcade
from mazegenerator import MazeGenerator


class Maze:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.maze: list[list[int]] = []
        self.width: int = width
        self.height: int = height
        self.seed: int = seed
        self.init_maze()

    def init_maze(self) -> None:
        maze = MazeGenerator((self.width, self.height), False)
        maze.generate(self.seed)
        self.maze = maze.maze

    def draw(self, window_width: float, window_height: float) -> None:
        m = window_height - 100
        size = m / self.height
        width_gap = (window_width - size * self.width) // 2
        height_gap = (window_height - size * self.height) // 2
        anc = arcade.Vec2()

        x, y = width_gap, window_height - height_gap - 50
        for _ in range(self.width):
            wall = arcade.XYWH(x, y, size, 5, anc)
            arcade.draw_rect_filled(wall, arcade.color.BLUE)
            x += size

        y = window_height - (height_gap + size) + 5 - 50
        for row in self.maze:
            x = width_gap - 5
            wall = arcade.XYWH(x, y, 5, size, anc)
            arcade.draw_rect_filled(wall, arcade.color.BLUE)
            x += size + 5
            for col in row:
                if col >> 1 & 1:
                    wall = arcade.XYWH(x, y, 5, size, anc)
                    arcade.draw_rect_filled(wall, arcade.color.BLUE)
                x += size
            x = width_gap
            for col in row:
                if col >> 2 & 1:
                    wall = arcade.XYWH(x, y, size, 5, anc)
                    arcade.draw_rect_filled(wall, arcade.color.BLUE)
                x += size
            y -= size
