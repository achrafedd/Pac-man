import arcade


class GameOver:
    def __init__(self, score: int, window: arcade.Window) -> None:
        self.user_name: str = ""
        self.score: int = score
        self.window: arcade.Window = window
        self.bg: arcade.Texture = arcade.load_texture("assets/background.jpeg")
        self.bg_rect: arcade.Rect = arcade.XYWH(
            0, 0, window.width, window.height
        )

    def draw(self) -> None:
        arcade.draw_texture_rect(self.bg, self.bg_rect)
        rect = arcade.XYWH(
            self.window.width // 2, self.window.height // 2, 350, 500
        )
        arcade.draw_rect_filled(rect, (00, 79, 79, 100))
