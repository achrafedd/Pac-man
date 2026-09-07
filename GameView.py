import arcade

from Ghost import Ghost
from Maze import Maze
from Player import Direction, Player
# from PauseMenu import PauseMenu
from Menu import PauseMenu
from typing import Any

class GameView(arcade.View):
    def __init__(self, maze: Maze, window: arcade.Window, config: dict[Any, Any]) -> None:
        super().__init__()
        self.maze: Maze = maze
        self.window = window
        self.config = config
        self.player: Player = Player((0, 0), maze, size=30)
        self.ghost_red: Ghost = Ghost((10, 10), maze, arcade.color.RED)
        self.ghost_blue: Ghost = Ghost((0, 5), maze, arcade.color.CYAN)
        self.ghost_pink: Ghost = Ghost((13, 0), maze, arcade.color.PINK)
        self.ghost_orange: Ghost = Ghost((7, 9), maze, arcade.color.ORANGE)
        self.bg: arcade.Texture = arcade.load_texture('assets/background.jpeg')
        self.bg_rect: arcade.Rect = arcade.XYWH(0, 0, self.width, self.height, arcade.Vec2())
                


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
        self.player.d += 5 * delta_time
        self.player.update(delta_time)

    def can_turn(self, x, y, dir):
        mask, _, _, _, _ = self.player.directions[dir.value]
        return not self.maze.maze[y][x] & mask

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            self.window.close()
        if symbol == arcade.key.ESCAPE:
            image = arcade.get_image()
            image.save("assets/Pausebg.png")
            self.window.show_view(PauseMenu(self.config, self))
        # Controle directions of player
        if symbol == arcade.key.UP:
            self.player.next_direction = Direction.UP
        if symbol == arcade.key.RIGHT:
            self.player.next_direction = Direction.RIGHT
        if symbol == arcade.key.DOWN:
            self.player.next_direction = Direction.DOWN
        if symbol == arcade.key.LEFT:
            self.player.next_direction = Direction.LEFT


