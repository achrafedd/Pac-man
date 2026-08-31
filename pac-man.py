import arcade

from GameView import Main_Menu
from Maze import Maze
from parser import check_config_values, check_file, parse_json, take_arges


def main() -> None:
    file = take_arges()
    data = check_file(file)
    config = parse_json(data)
    config = check_config_values(config)

    # window._update_rate = 1000
    window = arcade.Window(fullscreen=True)
    maze = Maze(config["width"], config["height"], config["seed"], window.width, window.height)
    menu = Main_Menu(maze, window)
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
    try:
        pass
    except Exception as e:
        print(f"Error: {e}")
