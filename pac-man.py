from typing import Any

import arcade
from pydantic import ValidationError

from GameOver import GameOver
from GameView import GameView
from LeaderBoard import LeaderBoard
from Maze import Maze
from Menu import MainMenu, PauseMenu
from utils import Stats, Config
from parser import Parser


class Pacman(arcade.Window):
    def __init__(self, config: Config, fullscreen: bool = False) -> None:
        super().__init__(fullscreen=fullscreen)
        self.__config: dict = config
        levels = config.levels
        self.maze = []
        # self.maze: Maze = Maze(
        #     config["width"],
        #     config["height"],
        #     config["seed"],
        #     self.width,
        #     self.height,
        # )
        self.menu: MainMenu = MainMenu(config, self)
        self.game: GameView = GameView(self.maze, self.menu, config, self)
        self.leaderboard: LeaderBoard = LeaderBoard("leaderboard.json", self)
        self.pause: PauseMenu = PauseMenu(self)
        self.game_over: GameOver = GameOver(
            config["highscore_filename"], self.game.player.score, self
        )
        self.stat: Stats = Stats.GAME_OVER

    def on_update(self, delta_time: float) -> None:
        if self.stat == Stats.GAME_VIEW:
            self.game.on_update(delta_time)

    def on_draw(self) -> None:
        self.clear()
        if self.stat == Stats.MAIN_MENU:
            del self.maze
            self.maze = Maze(
                self.__config["width"],
                self.__config["height"],
                self.__config["seed"],
                self.width,
                self.height,
            )
            self.game: GameView = GameView(
                self.maze, self.menu, self.__config, self
            )
            self.menu.on_draw()
        elif self.stat == Stats.GAME_VIEW:
            self.game.on_draw()
        elif self.stat == Stats.LEADERBOARD:
            self.leaderboard.leader_board = self.leaderboard.readfile()
            self.leaderboard.on_draw()
        elif self.stat == Stats.PAUSE_MENU:
            self.pause.on_draw()
        elif self.stat == Stats.GAME_OVER:
            self.game_over.on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.stat == Stats.MAIN_MENU:
            self.menu.on_key_press(symbol, modifiers)
        elif self.stat == Stats.GAME_VIEW:
            self.game.on_key_press(symbol, modifiers)
        elif self.stat == Stats.LEADERBOARD:
            self.leaderboard.on_key_press(symbol, modifiers)
        elif self.stat == Stats.PAUSE_MENU:
            self.pause.on_key_press(symbol, modifiers)
        elif self.stat == Stats.GAME_OVER:
            self.game_over.on_key_press(symbol, modifiers)


if __name__ == "__main__":
    try:
        p = Parser()
        arcade.load_font("assets/fonts/Pacmania.ttf")
        arcade.load_font("assets/fonts/PressStart2P-Regular.ttf")
        _ = Pacman(p.config, True)
        arcade.run()
    except ValidationError as e:
        print("Error:", e.errors()[0]['msg'])
    except BaseException as e:
        print(f"Error: {e}")
