from typing import Any

import arcade

from Ghost import Red_Ghost, Blue_Ghost, Orange_Ghost, Pink_Ghost
from Maze import Maze

from Menu import MainMenu
from Player import Direction, Player
from utils import Stats


class GameView:
    def __init__(
        self,
        maze: Maze,
        main_menu: MainMenu,
        config: dict[Any, Any],
        window: arcade.Window,
    ) -> None:
        super().__init__()
        self.maze: Maze = maze
        self.main_menu: MainMenu = main_menu
        self.config: dict = config
        self.window: arcade.Window = window
        self.player: Player = Player((10, 10), self.maze)
        self.ghost_red: Red_Ghost = Red_Ghost(
            (0, 1), self.maze, arcade.color.RED, self.player
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

    def game_over(self) -> bool:
        if (
            self.player.x == self.ghost_red.x
            and self.player.y == self.ghost_red.y
        ):
            return True
        if (
            self.player.x == self.ghost_blue.x
            and self.player.y == self.ghost_blue.y
        ):
            return True
        if (
            self.player.x == self.ghost_pink.x
            and self.player.y == self.ghost_pink.y
        ):
            return True
        if (
            self.player.x == self.ghost_orange.x
            and self.player.y == self.ghost_orange.y
        ):
            return True
        return False

    def on_draw(self) -> None:
        arcade.draw_text(f"SCORE: {self.player.score}", 100, 300)
        arcade.draw_texture_rect(self.bg, self.bg_rect)
        self.maze.draw(self.window.width, self.window.height)
        self.player.draw()
        self.ghost_red.draw()
        self.ghost_blue.draw()
        self.ghost_pink.draw()
        self.ghost_orange.draw()

    def on_update(self, delta_time: float) -> None:
        self.player.d += 5 * delta_time
        self.player.update(delta_time)
        self.ghost_red.update(delta_time)
        self.ghost_blue.update(delta_time)
        self.ghost_pink.update(delta_time)
        self.ghost_orange.update(delta_time)

    def can_turn(self, x: float, y: float, direction: Direction):
        mask, _, _, _, _ = self.player.directions[direction.value]
        return not self.maze.maze[y][x] & mask

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
