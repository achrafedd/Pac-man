import json
from typing import Any

import arcade


class LeaderBoard(arcade.View):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.file: str = file
        self.leader_board: Any = self.readfile()


    def readfile(self) -> Any:
        data = {}
        with open(self.file) as file:
            data = json.load(file)
        data = sorted(data, key=lambda x: x['score'], reverse=True)
        return data


    def cart(self, x, y, rank: int, name: str, score: int):
        cart = arcade.XYWH(
                    x, y,
                    200,
                    80
                )
        arcade.draw_rect_outline(cart, arcade.color.YELLOW)
        arcade.draw_text(
                f"{rank} {name}",
                x - 80, y,
                arcade.color.WHITE,
                12,
                font_name="Press Start 2P",
                anchor_y='center'
                )

    def on_draw(self) -> None:
        self.clear()
        arcade.draw_text(
                'LEADER BOARD',
                self.width // 2,
                self.height - 100,
                arcade.color.YELLOW,
                50,
                font_name="pacmania",
                anchor_x='center',
                anchor_y='center'
                )
        x, y = self.width // 2, self.height - 200
        for idx, element in enumerate(self.leader_board, start=1):
            self.cart(
                    x, y - (idx * 100),
                    idx,
                    element['name'],
                    element['score']
                    )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            self.window.close()
