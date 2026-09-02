import arcade

from GameView import GameView
from LeaderBoard import LeaderBoard
from Maze import Maze


class Main_Menu(arcade.View):
    def __init__(self, maze: Maze, window: arcade.Window):
        self.window: arcade.Window = window
        super().__init__()
        self.menu_list: dict[str, arcade.View | None] = {
                "start game": GameView(maze),
                "high score": LeaderBoard('leaderboard.json'),
                "settings": None,
                "exit": None
                }
        self.__index: int = 0
        self.gap: float = 0
        self.sprites = arcade.SpriteList()
        self.maze: Maze = maze
        # arcade.set_background_color(arcade.color.DARK_BLUE)
        self.background: arcade.Texture = arcade.load_texture('assets/background.jpeg')
        self.bg_rect: arcade.Rect = arcade.XYWH(0, 0, self.width, self.height, arcade.Vec2())
        self.selector: arcade.Texture = arcade.load_texture('assets/pacman.png')

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, self.bg_rect)
        self.draw_menu()

    def on_key_press(self, symbol: int, modifiers):
        self.draw_menu()
        if symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.MOTION_DOWN or symbol == arcade.key.J:
            self.__index = (self.__index + 1) % 4
            self.gap = (self.gap + 100) % (100*4)
        elif symbol == arcade.key.MOTION_UP or symbol == arcade.key.K:
            self.__index = (self.__index - 1) % 4
            self.gap = (self.gap - 100) % (100*4)
        elif symbol == arcade.key.ENTER:
            if self.__index != 3:
                item: str = list(self.menu_list.keys())[self.__index]
                self.window.show_view(self.menu_list[item])
            else:
                self.window.close()

    def button(self,
               x: float,
               y: float,
               text: str
               ) -> None:
        button = arcade.XYWH(x, y, 200, 80)
        arcade.draw_rect_filled(
                button,
                arcade.color.DARK_BLUE
                )
        arcade.draw_rect_outline(
                button,
                arcade.color.CYAN
                )
        arcade.draw_text(
                text,
                x,
                y,
                arcade.color.WHITE,
                12,
                font_name="Press Start 2P",
                anchor_x='center',
                anchor_y='center'
                )

    def draw_menu(self):
        x = self.width // 2
        arcade.draw_text(
                'Pac-man',
                x,
                self.height - 100,
                arcade.color.YELLOW,
                50,
                font_name="pacmania",
                anchor_x='center',
                anchor_y='center'
                )
        for idx, title in enumerate(self.menu_list):
            self.button(
                    x,
                    500 - (idx * 100),
                    title.upper()
                    )
        selector_rect = arcade.XYWH(x - 180, 500 - self.gap, 30, 30)
        arcade.draw_texture_rect(self.selector, selector_rect)
