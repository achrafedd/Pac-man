import arcade

from .Maze import Maze


class GameView(arcade.View):
    def __init__(self, maze: Maze) -> None:
        super().__init__()
        self.maze: Maze = maze

    def on_draw(self) -> None:
        self.clear()
        self.maze.draw(self.width, self.height)

    def on_update(self, delta_time: float) -> None:
        pass

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            exit(0)
