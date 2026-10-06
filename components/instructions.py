import arcade

from components.utils import Stats


class Instructions:
    """Represent instructions behavior.
    """
    def __init__(self, window: arcade.Window) -> None:
        """Initialize the object.

        Args:
            window (arcade.Window): Value used by the operation.
        """
        self.window: arcade.Window = window
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
            1000,
            1000,
        )
        arcade.draw_rect_filled(rect, (00, 79, 79, 200))
        arcade.draw_rect_outline(rect, (250, 226, 81))
        self._draw_text(
            "How To Play",
            self.window.width // 2 - 200,
            self.window.height // 2 + 400,
            30,
            arcade.color.RED,
        )
        self._draw_text(
            "MOVE :",
            self.window.width // 2 - 450,
            self.window.height // 2 + 300,
            18,
            arcade.color.YELLOW,
        )
        self._draw_text(
            "USE ARROW KEYS",
            self.window.width // 2 - 250,
            self.window.height // 2 + 300,
            18,
            arcade.color.WHITE,
        )
        self._draw_text(
            "PAUSE :",
            self.window.width // 2 - 450,
            self.window.height // 2 + 200,
            18,
            arcade.color.YELLOW,
        )
        self._draw_text(
            "PRESS ESC TO PAUSE",
            self.window.width // 2 - 250,
            self.window.height // 2 + 200,
            18,
            arcade.color.WHITE,
        )
        self._draw_text(
            "MAIN MENU:",
            self.window.width // 2 - 450,
            self.window.height // 2 + 100,
            18,
            arcade.color.YELLOW,
        )
        self._draw_text(
            "PRESS M TO GO TO MAIN MENU",
            self.window.width // 2 - 200,
            self.window.height // 2 + 100,
            18,
            arcade.color.WHITE,
        )
        self._draw_text(
            "EXIT :",
            self.window.width // 2 - 450,
            self.window.height // 2,
            18,
            arcade.color.YELLOW,
        )
        self._draw_text(
            "PRESS Q TO QUIT",
            self.window.width // 2 - 250,
            self.window.height // 2,
            18,
            arcade.color.WHITE,
        )
        self._draw_text(
            "GOAL :",
            self.window.width // 2 - 450,
            self.window.height // 2 - 100,
            18,
            arcade.color.YELLOW,
        )
        self._draw_text(
            "SCORE HIGH & AVOID GHOSTS",
            self.window.width // 2 - 250,
            self.window.height // 2 - 100,
            18,
            arcade.color.WHITE,
        )
        self._draw_text(
            "CHEAT MODE :",
            self.window.width // 2 - 450,
            self.window.height // 2 - 200,
            18,
            arcade.color.RED,
        )
        self._draw_text(
            "PRESS C TO BE IVESIBLE",
            self.window.width // 2 - 350,
            self.window.height // 2 - 280,
            18,
            arcade.color.YELLOW,
        )
        self._draw_text(
            "PRESS N TO SKIP LEVEL",
            self.window.width // 2 - 350,
            self.window.height // 2 - 360,
            18,
            arcade.color.YELLOW,
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Perform the on key press operation.

        Args:
            symbol (int): Value used by the operation.
            modifiers (int): Value used by the operation.
        """
        if symbol == arcade.key.M:
            self.window.stat = Stats.MAIN_MENU
        elif symbol == arcade.key.Q:
            self.window.stat = Stats.EXIT

    def _draw_text(
        self,
        text: str,
        x: float,
        y: float,
        size: int,
        color: arcade.types.Color,
    ) -> None:
        """Perform the draw text operation.

        Args:
            text (str): Value used by the operation.
            x (float): Value used by the operation.
            y (float): Value used by the operation.
            size (int): Value used by the operation.
            color (arcade.types.Color): Value used by the operation.
        """
        obj = arcade.Text(
            text,
            x,
            y,
            color,
            size,
            anchor_x="left",
            anchor_y="center",
            font_name="Press Start 2P",
        )
        obj.draw()
