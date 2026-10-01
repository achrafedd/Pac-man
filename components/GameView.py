import arcade
from .Ghost import Red_Ghost, Blue_Ghost, Orange_Ghost, Pink_Ghost, Ghost
from .Maze import Maze

from .Menu import MainMenu
from .Player import Direction, Player
from .utils import Config, Stats


class GameView:
    def __init__(
        self,
        config: Config,
        maze: Maze,
        main_menu: MainMenu,
        window: arcade.Window,
    ) -> None:
        super().__init__()
        self.maze: Maze = maze
        self.main_menu: MainMenu = main_menu
        self.config: Config = config
        self.lives_remaining: int = config.lives
        self.time: int = config.level_max_time
        self.window: arcade.Window = window
        self.restart: bool = True
        self.isCounting: bool = True
        self.counter: float = 3
        self.player: Player = Player((3, 3), self.maze)
        self.left_top_flag: bool = True
        self.right_top_flag: bool = True
        self.left_down_flag: bool = True
        self.right_down_flag: bool = True
        self.super_power: bool = False
        self.run_time: int = 6


        self.ghost_red: Red_Ghost = Red_Ghost(
            (0, 0), self.maze, arcade.color.RED, self.player
        )
        self.ghost_blue: Blue_Ghost = Blue_Ghost(
            (self.maze.width - 1, self.maze.height - 1),
            self.maze,
            arcade.color.CYAN,
            self.player,
            self.ghost_red,
        )
        self.ghost_pink: Pink_Ghost = Pink_Ghost(
            (self.maze.width - 1, 0), self.maze, arcade.color.PINK, self.player
        )
        self.ghost_orange: Orange_Ghost = Orange_Ghost(
            (0, self.maze.height - 1),
            self.maze,
            arcade.color.ORANGE,
            self.player,
        )
        self.bg: arcade.Texture = arcade.load_texture("assets/background.jpeg")
        self.bg_rect: arcade.Rect = arcade.XYWH(
            0, 0, window.width, window.height, arcade.Vec2()
        )

    def _init_game(self):
        self.lives_remaining = self.config.lives
        self.time = self.config.level_max_time
        self.isCounting = True
        self.ghost_blue._restart()
        self.ghost_red._restart()
        self.ghost_orange._restart()
        self.ghost_pink._restart()
        self.player._restart()

    def _distance(self, player: Player, ghost: Ghost):
        return (
            (ghost.pixel_x - player.pixel_x) ** 2
            + (ghost.pixel_y - player.pixel_y) ** 2
        ) ** (1 / 2)

    def game_over(self) -> bool:
        if (self.super_power or self.player.cheat_mode):
            return False
        if (
            self._distance(self.player, self.ghost_red)<= 30
            ):
            return True
        if self._distance(self.player, self.ghost_blue) <= 30:
            return True
        if self._distance(self.player, self.ghost_pink) <= 30:
            return True
        if self._distance(self.player, self.ghost_orange) <= 30:
            return True
        return False

    def on_draw(self) -> None:
        arcade.draw_texture_rect(self.bg, self.bg_rect)
        self.maze.draw()
        self.player.draw()
        self.ghost_red.draw()
        self.ghost_blue.draw()
        self.ghost_pink.draw()
        self.ghost_orange.draw()
        self._draw_hud()
        if self.isCounting:
            counter = arcade.Text(
                str(int(self.counter)),
                self.window.width // 2,
                self.window.height // 2,
                font_name="Press Start 2P",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
            )
            counter.draw()

    def counting(self, delta_time: float) -> None:
        self.counter -= delta_time
        if self.counter < 0:
            self.isCounting = False
            self.restart = True
            self.counter = 3

    def super_gum(self):
        if self.maze.gums[0][0] == 0 and self.left_top_flag:
            self.run_time = 6
            self.left_top_flag = False
            self.super_power = True
            self.ghost_blue.fear = True
            self.ghost_red.fear = True
            self.ghost_orange.fear = True
            self.ghost_pink.fear = True
        elif self.maze.gums[self.maze.height - 1][0] == 0 and self.left_down_flag:
            self.run_time = 6
            self.left_down_flag = False
            self.super_power = True
            self.ghost_blue.fear = True
            self.ghost_red.fear = True
            self.ghost_orange.fear = True
            self.ghost_pink.fear = True
        elif self.maze.gums[0][self.maze.width - 1] == 0 and self.right_top_flag:
            self.run_time = 6
            self.right_top_flag = False
            self.super_power = True
            self.ghost_blue.fear = True
            self.ghost_red.fear = True
            self.ghost_orange.fear = True
            self.ghost_pink.fear = True
        elif self.maze.gums[self.maze.height - 1][self.maze.width - 1] == 0 and self.right_down_flag:
            self.run_time = 6
            self.right_down_flag = False
            self.super_power = True
            self.ghost_blue.fear = True
            self.ghost_red.fear = True
            self.ghost_orange.fear = True
            self.ghost_pink.fear = True
            


    def on_update(self, delta_time: float) -> None:
        if self.isCounting:
            self.counting(delta_time)
            return
        self.player.d += 5 * delta_time
        self.player.update(delta_time)
        self.ghost_red.update(delta_time)
        self.ghost_blue.update(delta_time)
        self.ghost_pink.update(delta_time)
        self.ghost_orange.update(delta_time)
        if self.game_over() and self.restart:
            if self.lives_remaining == 1:
                self.window.stat = Stats.GAME_OVER
            else:
                self.restart = False
                self.lives_remaining -= 1
                self.player._restart()
                self.ghost_blue._restart()
                self.ghost_red._restart()
                self.ghost_pink._restart()
                self.ghost_orange._restart()
                self.isCounting = True
        self.super_gum()
        if self.super_power and self.run_time > 0:
            self.run_time -= delta_time
            if self.run_time <= 0:
                self.super_power = False
                self.ghost_blue.fear = False
                self.ghost_red.fear = False
                self.ghost_orange.fear = False
                self.ghost_pink.fear = False
                self.run_time = 6



    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            self.window.close()
        if symbol == arcade.key.ESCAPE:
            image = arcade.get_image()
            image.save("assets/Pausebg.png")
            self.window.stat = Stats.PAUSE_MENU
        # Controle directions of player
        if symbol == arcade.key.UP:
            self.player.next_direction = Direction.UP
            self.player.dir = 0
        if symbol == arcade.key.RIGHT:
            self.player.dir = 1
            self.player.next_direction = Direction.RIGHT
        if symbol == arcade.key.DOWN:
            self.player.dir = 2
            self.player.next_direction = Direction.DOWN
        if symbol == arcade.key.LEFT:
            self.player.dir = 3
            self.player.next_direction = Direction.LEFT
        if symbol == arcade.key.N:
            self.window.skip = True
        if symbol == arcade.key.C:
            self.player.cheat_mode = not self.player.cheat_mode

    def _draw_hud(self):
        rect = arcade.XYWH(
            0, self.window.height - 80, self.window.width, 80, arcade.Vec2()
        )
        arcade.draw_rect_filled(rect, (33, 33, 33, 180))
        for i in range(self.config.lives):
            if i < self.lives_remaining:
                color = (250, 226, 81)
            else:
                color = (250, 226, 81, 150)
            arcade.draw_circle_filled(
                self.window.width * 0.20 - (40 * i),
                self.window.height - 40,
                15,
                color,
            )
        score = arcade.Text(
            f"Score: {self.player.score}",
            self.window.width * 0.40,
            self.window.height - 40,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
        )
        score.draw()
        level = arcade.Text(
            f"Level: {self.window.current_level}",
            self.window.width * 0.60,
            self.window.height - 40,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
        )
        level.draw()
        time = arcade.Text(
            f"Time: {self.time}",
            self.window.width * 0.80,
            self.window.height - 40,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
        )
        time.draw()
