import arcade

from .GameView import GameView
from .Maze import Maze


def main() -> None:
    maze = Maze(30, 20, 42)
    window = arcade.Window(fullscreen=True)
    game_view = GameView(maze)
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
