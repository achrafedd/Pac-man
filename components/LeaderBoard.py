import json
from typing import Any

import arcade

from .utils import LeaderBoardSchema, Stats


class LeaderBoard:
    def __init__(self, file: str, window: arcade.Window) -> None:
        super().__init__()
        self.window: arcade.Window = window
        self.file: str = file
        self.leader_board: Any = self.readfile()
        self.start: int = 0
        self.end: int = 10
        self.bg: arcade.Texture = arcade.load_texture("assets/background.jpeg")
        self.crown: arcade.Texture = arcade.load_texture("assets/crown.png")
        self.cup: arcade.Texture = arcade.load_texture("assets/cup.png")
        self.medal: arcade.Texture = arcade.load_texture("assets/medal.png")
        self.bg_rect: arcade.Rect = arcade.XYWH(
            0, 0, window.width, window.height, arcade.Vec2()
        )

    def readfile(self) -> Any | None:
        data: Any = {}
        try:
            with open(self.file) as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return None

        data = sorted(data, key=lambda x: x["score"], reverse=True)
        res = [LeaderBoardSchema(**el) for el in data]
        return res

    def score_row(
            self,
            x: float,
            y: float,
            rank: int,
            name: str,
            score: int
            ) -> None:
        rect = arcade.XYWH(x - 300, y, 50, 50)
        if rank == 1:
            arcade.draw_texture_rect(self.crown, rect)
        elif rank == 2:
            arcade.draw_texture_rect(self.cup, rect)
        elif rank == 3:
            arcade.draw_texture_rect(self.medal, rect)
        else:
            rand_text = arcade.Text(
                str(rank),
                x - 300,
                y,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                font_name="Press Start 2P",
                anchor_y="center",
            )
            rand_text.draw()
        name_text = arcade.Text(
            name,
            x,
            y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            font_name="Press Start 2P",
            anchor_y="center",
        )
        name_text.draw()
        score_text = arcade.Text(
            str(score),
            x + 300,
            y,
            arcade.color.WHITE,
            20,
            anchor_x="right",
            font_name="Press Start 2P",
            anchor_y="center",
        )
        score_text.draw()

    def on_draw(self) -> None:
        arcade.draw_texture_rect(self.bg, self.bg_rect)
        rect = arcade.XYWH(
            self.window.width // 2,
            self.window.height // 2 - 50,
            700,
            self.window.height - 300,
        )
        arcade.draw_rect_filled(rect, (0, 0, 0, 150))
        arcade.draw_rect_outline(rect, arcade.color.WHITE)
        text = arcade.Text(
            "LEADER BOARD",
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.YELLOW,
            50,
            font_name="pacmania",
            anchor_x="center",
            anchor_y="center",
        )
        text.draw()
        x, y = self.window.width // 2, self.window.height - 200
        if self.leader_board is None:
            empty = arcade.Text(
                "Leader Board is empty",
                self.window.width // 2,
                self.window.height // 2,
                arcade.color.YELLOW,
                18,
                font_name="Press Start 2P",
                anchor_x="center",
                anchor_y="center",
            )
            empty.draw()
            return

        for idx, element in enumerate(
            self.leader_board[self.start: self.end], start=1
        ):
            self.score_row(
                x,
                y - (idx * 70),
                idx + self.start,
                element.name,
                element.score,
            )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.DOWN:
            if self.end < len(self.leader_board):
                self.start += 1
                self.end += 1
        elif symbol == arcade.key.UP:
            if self.start > 0:
                self.start -= 1
                self.end -= 1
        elif symbol == arcade.key.M:
            self.window.stat = Stats.MAIN_MENU
