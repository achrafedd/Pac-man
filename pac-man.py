import arcade

from GameView import GameView
from Maze import Maze
from parser import check_config_values, take_arges, check_file, parse_json


def main() -> None:
    file = take_arges()
    data = check_file(file)
    config = parse_json(data)
    config = check_config_values(config)

    maze = Maze(config["width"], config["height"], config["seed"])
    window = arcade.Window(fullscreen=True)
    game_view = GameView(maze)
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
