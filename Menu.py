from typing import Any

import arcade
import cv2

from LeaderBoard import LeaderBoard
from Maze import Maze


class Main_Menu(arcade.View):
    def __init__(self, config: dict[Any, Any]):
        super().__init__()
        from GameView import GameView
        self.maze = Maze(config["width"], config["height"], config["seed"], self.window.width, self.window.height)
        self.menu_list: dict[str, arcade.View | None] = {
                "start game": GameView(self.maze, self, config),
                "high score": LeaderBoard('leaderboard.json'),
                "settings": None,
                "exit": None
                }
        self.__index: int = 0
        self.gap: float = 0
        self.sprites = arcade.SpriteList()
        # arcade.set_background_color(arcade.color.DARK_BLUE)
        self.background: arcade.Texture = arcade.load_texture('assets/background.jpeg')
        self.bg_rect: arcade.Rect = arcade.XYWH(0, 0, self.width, self.height, arcade.Vec2())
        self.selector: arcade.Texture = arcade.load_texture('assets/pacman.png')

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, self.bg_rect)
        self.draw_menu()

    def on_key_press(self, symbol: int, modifiers):
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
        # arcade.draw
        arcade.draw_rect_outline(
            arcade.XYWH(self.width//2, (self.height // 2)-100, 450, 800),
            arcade.color.DARK_BLUE
        )
        arcade.draw_lrbt_rectangle_filled((self.width//2)-225,(self.width//2)+225, (self.height//2)-500, (self.height//2)+300, (0, 0, 0, 150))
        arcade.draw_text(
                'Pac-man',
                x,
                self.height - 300,
                arcade.color.YELLOW,
                60,
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
        selector_rect = arcade.XYWH(x - 180, 500 - self.gap, 40, 40)
        arcade.draw_texture_rect(self.selector, selector_rect)


class PauseMenu(arcade.View):
    def __init__(self, game, config):
        super().__init__()
        self.config = config
        self.menu_list : dict[Any, Any]= {
            "Resume the game": game,
            "Return to the main menu": Main_Menu(config),
            }
        self.__index: int = 0
        self.gap: float = 0
        self.selector: arcade.Texture = arcade.load_texture('assets/pacman.png')
        self.blur_bg()

    def blur_bg(self):
        img = cv2.imread("assets/Pausebg.png")
        img = cv2.GaussianBlur(img, (21, 21), 0)
        cv2.imwrite("assets/Pausebg.png", img)
        self.background = arcade.load_texture("assets/Pausebg.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.rect.XYWH(
            self.window.width / 2,
            self.window.height / 2,
            self.window.width,
            self.window.height,
        ),)
        self.draw_menu()

    def draw_menu(self):
        x = self.width // 2
        # arcade.draw
        arcade.draw_rect_outline(
             arcade.XYWH(
                  self.width//2,
                  (self.height // 2),
                  450,
                  700
                  ),
                  arcade.color.YELLOW
                  )
        arcade.draw_lrbt_rectangle_filled(
             (self.width//2) - 225,
             (self.width//2) + 225,
             (self.height//2) - 350,
             (self.height//2) + 350,
             (0, 0, 0, 150)
             )
        arcade.draw_text(
                'Paused',
                x,
                self.height - 300,
                arcade.color.YELLOW,
                60,
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
        selector_rect = arcade.XYWH(x - 180, 500 - self.gap, 50, 50)
        arcade.draw_texture_rect(self.selector, selector_rect)

    def button(
            self,
            x: float,
            y: float,
            text: str) -> None:
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
                    10,
                    font_name="Press Start 2P",
                    anchor_x='center',
                    anchor_y='center'
                    )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.MOTION_DOWN or symbol == arcade.key.J:
                    self.__index = (self.__index + 1) % 2
                    self.gap = (self.gap + 100) % (100*2)
        elif symbol == arcade.key.MOTION_UP or symbol == arcade.key.K:
            self.__index = (self.__index - 1) % 2
            self.gap = (self.gap - 100) % (100*2)
        elif symbol == arcade.key.ENTER:
            if self.__index != 3:
                item: str = list(self.menu_list.keys())[self.__index]
                self.window.show_view(self.menu_list[item])
            else:
                self.window.close()
