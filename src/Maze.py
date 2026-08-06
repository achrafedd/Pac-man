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
        print(self.maze)

    def draw(self, window_width: int, window_height: int) -> None:
        wall_width = abs((window_width - 200) / len(self.maze[0]))
        wall_height = abs((window_height - 100) / len(self.maze))
        anc = arcade.Vec2()

        x, y = 100, window_height - 50
        for _ in range(len(self.maze[0])):
            wide_rect = arcade.XYWH(x, y, wall_width, 2, anc)
            arcade.draw_rect_filled(wide_rect, arcade.color.BLUE)
            x += wall_width

        y = window_height - (50 + wall_height)
        for row in self.maze:
            x = 100
            wide_rect = arcade.XYWH(x, y, 2, wall_height, anc)
            arcade.draw_rect_filled(wide_rect, arcade.color.BLUE)
            x += wall_width
            for cell in row:
                if cell >> 1 & 1:
                    wide_rect = arcade.XYWH(x, y, 2, wall_height, anc)
                    arcade.draw_rect_filled(wide_rect, arcade.color.BLUE)
                x += wall_width
            y -= wall_height
            x = 100
            for cell in row:
                if cell >> 2 & 1:
                    wide_rect = arcade.XYWH(x, y, wall_width, 2, anc)
                    arcade.draw_rect_filled(wide_rect, arcade.color.BLUE)
                x += wall_width
