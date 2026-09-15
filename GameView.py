from typing import Any

import arcade

from Ghost import Red_Ghost, Blue_Ghost, Orange_Ghost, Pink_Ghost
from Maze import Maze

# from PauseMenu import PauseMenu
from Menu import PauseMenu
from Player import Direction, Player


class GameView(arcade.View):
    def __init__(self, maze: Maze, Main_menu, config: dict[Any, Any]) -> None:
        super().__init__()
        self.maze = maze
        self.main_menu = Main_menu
        self.config = config
        self.player: Player = Player((10, 10), self.maze)
        self.ghost_red: Red_Ghost = Red_Ghost((0, 1), self.maze, arcade.color.RED, self.player)
        self.ghost_blue: Blue_Ghost = Blue_Ghost((self.maze.width - 1, self.maze.height - 1), self.maze, arcade.color.CYAN, self.player, self.ghost_red)
        self.ghost_pink: Pink_Ghost = Pink_Ghost((self.maze.width - 1, 0), self.maze, arcade.color.PINK, self.player)
        self.ghost_orange: Orange_Ghost = Orange_Ghost((0, self.maze.height - 1), self.maze, arcade.color.ORANGE, self.player)
        self.bg: arcade.Texture = arcade.load_texture('assets/background.jpeg')
        self.bg_rect: arcade.Rect = arcade.XYWH(0, 0, self.width, self.height, arcade.Vec2())
    def game_over(self) -> bool:
        if self.player.x == self.ghost_red.x and self.player.y == self.ghost_red.y:
            return True
        if self.player.x == self.ghost_blue.x and self.player.y == self.ghost_blue.y:
            return True
        if self.player.x == self.ghost_pink.x and self.player.y == self.ghost_pink.y:
            return True
        if self.player.x == self.ghost_orange.x and self.player.y == self.ghost_orange.y:
            return True
        return False

    def on_draw(self) -> None:
        self.clear()
        arcade.draw_texture_rect(self.bg, self.bg_rect)
        arcade.draw_text(
                f"SCORE: {self.player.score}",
                100,
                300
                )
        self.maze.draw(self.width, self.height)
        self.player.draw()
        self.ghost_red.draw()
        self.ghost_blue.draw()
        self.ghost_pink.draw()
        self.ghost_orange.draw()

    def on_update(self, delta_time: float) -> None:
        if (self.game_over()):
            print("Game Over")
            self.window.close()
        self.player.d += 5 * delta_time
        self.player.update(delta_time)
        # self.ghost_red.update(delta_time)
        # self.ghost_blue.update(delta_time)
        self.ghost_pink.update(delta_time)
        self.ghost_orange.update(delta_time)

    def can_turn(self, x, y, dir):
        mask, _, _, _, _ = self.player.directions[dir.value]
        return not self.maze.maze[y][x] & mask

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            self.window.close()
        if symbol == arcade.key.ESCAPE:
            image = arcade.get_image()
            image.save("assets/Pausebg.png")
            self.window.show_view(PauseMenu(self, self.config))
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
