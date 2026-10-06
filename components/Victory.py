import json
from typing import Any

import arcade

from .utils import LeaderBoardSchema, Stats


class Victory:
    """Represent victory behavior.
    """
    def __init__(self, file: str, score: int, window: arcade.Window) -> None:
        """Initialize the object.

        Args:
            file (str): Value used by the operation.
            score (int): Value used by the operation.
            window (arcade.Window): Value used by the operation.
        """
        self.user_name: str = ""
        self.file: str = file
        self.score: int = score
        self.window: arcade.Window = window
        self.name: str = ""
        self.bg: arcade.Texture = arcade.load_texture("assets/background.jpeg")
        self.bg_rect: arcade.Rect = arcade.XYWH(
            0, 0, window.width, window.height, arcade.Vec2()
        )

    def on_draw(self) -> None:
        """Perform the on draw operation.
        """
        arcade.draw_texture_rect(self.bg, self.bg_rect)
        rect = arcade.XYWH(
            self.window.width // 2,
            self.window.height // 2,
            500,
            500,
        )
        arcade.draw_rect_filled(rect, (00, 79, 79, 200))
        arcade.draw_rect_outline(rect, (250, 226, 81))
        head = arcade.Text(
            "Victory",
            self.window.width // 2,
            self.window.height // 2 + 200,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
            font_size=25,
            color=arcade.color.RED,
        )
        score = arcade.Text(
            f"Final Score: {self.score}",
            self.window.width // 2,
            self.window.height // 2 + 120,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
            font_size=18,
        )
        label_name = arcade.Text(
            "Enter Your Name",
            self.window.width // 2,
            self.window.height // 2 + 40,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
            font_size=14,
        )
        head.draw()
        score.draw()
        label_name.draw()
        input_rect = arcade.XYWH(
            self.window.width // 2, self.window.height // 2 - 20, 400, 40
        )
        arcade.draw_rect_outline(
            input_rect, arcade.color.WHITE, border_width=3
        )
        name = arcade.Text(
            f"{self.name}_",
            self.window.width // 2 - 190,
            self.window.height // 2 - 20,
            anchor_x="left",
            anchor_y="center",
            font_name="Press Start 2P",
            font_size=14,
        )
        name.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Perform the on key press operation.

        Args:
            symbol (int): Value used by the operation.
            modifiers (int): Value used by the operation.
        """
        if symbol == arcade.key.ESCAPE:
            self.window.close()
        if len(self.name) < 10:
            if symbol >= arcade.key.A and symbol <= arcade.key.Z:
                self.name += chr(symbol)
            if symbol == arcade.key.SPACE:
                self.name += " "
            if symbol >= arcade.key.KEY_1 and symbol <= arcade.key.KEY_9:
                self.name += chr(symbol)
        if symbol == arcade.key.BACKSPACE:
            self.name = self.name[:-1]
        if symbol == arcade.key.ENTER:
            self._save_score()

    def _save_score(self) -> None:
        """Perform the save score operation.
        """
        data: LeaderBoardSchema = LeaderBoardSchema(
            name=self.name, score=self.score
        )
        try:
            with open(self.file) as file:
                res: Any = json.load(file)
        except BaseException:
            res = []
        res.append(data.model_dump())
        with open(self.file, "w+") as file:
            json.dump(res, file, indent=4)
            self.name = ""
            self.window.stat = Stats.MAIN_MENU
