import arcade
from pydantic import ValidationError

from components import GameOver
from components import GameView
from components import LeaderBoard
from components import Maze
from components import MainMenu, PauseMenu
from components import Victory
from components import Stats, Config
from components import Parser
from components import Instructions


class Pacman(arcade.Window):
    """Represent pacman behavior.
    """
    def __init__(self, config: Config, fullscreen: bool = False) -> None:
        """Initialize the object.

        Args:
            config (Config): Value used by the operation.
            fullscreen (bool): Value used by the operation.
        """
        super().__init__(fullscreen=fullscreen)
        self.con: Config = config
        self.menu: MainMenu = MainMenu(self)
        self.current_level: int = len(config.levels)
        self.lives_remaining: int = config.lives
        self.score: int = 0
        self.skip: bool = False
        self.mazes: list[Maze] = [
            Maze(
                config.levels[i]["width"],
                config.levels[i]["height"],
                config,
                config.seed,
                self.width,
                self.height,
            )
            for i in range(len(config.levels))
        ]
        self.games: list[GameView] = [
            GameView(config, self.mazes[i], self.menu, self)
            for i in range(len(config.levels))
        ]
        self.leaderboard: LeaderBoard = LeaderBoard(
            config.highscore_filename, self
        )
        self.pause: PauseMenu = PauseMenu(self)
        self.game_over: GameOver = GameOver(
            config.highscore_filename,
            self.score,
            self,
        )
        self.victory: Victory = Victory(
            config.highscore_filename,
            self.score,
            self,
        )
        self.instructions: Instructions = Instructions(self)
        self.stat: Stats = Stats.MAIN_MENU

    def on_update(self, delta_time: float) -> None:
        """Perform the on update operation.

        Args:
            delta_time (float): Value used by the operation.
        """
        if self.stat == Stats.GAME_VIEW:
            self.games[self.current_level - 1].on_update(delta_time)
            self._skip_level()

    def on_draw(self) -> None:
        """Perform the on draw operation.
        """
        self.clear()
        if self.stat == Stats.MAIN_MENU:
            self.lives_remaining = self.con.lives
            self.current_level = 1
            for maze in self.mazes:
                maze.init_gums()
            for game in self.games:
                game._init_game()
            self.menu.on_draw()
        elif self.stat == Stats.GAME_VIEW:
            self.games[self.current_level - 1].on_draw()
        elif self.stat == Stats.LEADERBOARD:
            self.leaderboard.leader_board = self.leaderboard.readfile()
            self.leaderboard.on_draw()
        elif self.stat == Stats.PAUSE_MENU:
            self.pause.on_draw()
        elif self.stat == Stats.GAME_OVER:
            self.game_over.score = self.score
            self.game_over.on_draw()
        elif self.stat == Stats.VICTORY:
            self.victory.score = self.score
            self.victory.on_draw()
        elif self.stat == Stats.INSTRUCTIONS:
            self.instructions.on_draw()
        elif self.stat == Stats.EXIT:
            self.close()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Perform the on key press operation.

        Args:
            symbol (int): Value used by the operation.
            modifiers (int): Value used by the operation.
        """
        if self.stat == Stats.MAIN_MENU:
            self.menu.on_key_press(symbol, modifiers)
        elif self.stat == Stats.GAME_VIEW:
            self.games[self.current_level - 1].on_key_press(symbol, modifiers)
        elif self.stat == Stats.LEADERBOARD:
            self.leaderboard.on_key_press(symbol, modifiers)
        elif self.stat == Stats.PAUSE_MENU:
            self.pause.on_key_press(symbol, modifiers)
        elif self.stat == Stats.GAME_OVER:
            self.game_over.on_key_press(symbol, modifiers)
        elif self.stat == Stats.INSTRUCTIONS:
            self.instructions.on_key_press(symbol, modifiers)
        elif self.stat == Stats.VICTORY:
            self.victory.on_key_press(symbol, modifiers)

    def _skip_level(self) -> None:
        """Perform the skip level operation.
        """
        if (
            not any(
                any(row) for row in self.mazes[self.current_level - 1].gums
            )
            or self.skip
        ):
            self.skip = False
            self.current_level += 1
            if self.current_level > len(self.con.levels):
                self.current_level = 1
                self.stat = Stats.VICTORY


if __name__ == "__main__":
    try:
        p = Parser()
        arcade.load_font("assets/fonts/Pacmania.ttf")
        arcade.load_font("assets/fonts/PressStart2P-Regular.ttf")
        _ = Pacman(p.config, True)
        arcade.run()
    except ValidationError as e:
        print("Error:", e.errors()[0]["msg"])
    except BaseException as e:
        print(f"Error: {e}")
