import arcade

from Maze import Maze


class GameView(arcade.View):
    def __init__(self, maze: Maze) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.TRANSPARENT_BLACK)
        self.maze: Maze = maze

    def on_draw(self) -> None:
        self.clear()
        anc = arcade.Vec2()
        banner = arcade.XYWH(0, self.height - 75, self.width, 75, anc)
        arcade.draw_rect_filled(banner, arcade.color.BLUE_BELL)
        self.maze.draw(self.width, self.height)

    def on_update(self, delta_time: float) -> None:
        pass

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            exit(0)


class Main_Menu(arcade.View):
    def __init__(self, maze, window):
        self.window = window
        super().__init__()
        self.menu_list = [
            GameView(maze),
            "view_highscore",
            "Instruction",
            "exit"
            ]
        self.__index = 0
        self.gap = 0
        self.sprites = arcade.SpriteList()
        self.maze = maze
        # arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        self.draw_menu()

    def on_key_press(self, symbol, modifiers):
        self.draw_menu()
        if symbol == arcade.key.MOTION_DOWN or symbol == arcade.key.J:
            self.__index = (self.__index + 1) % 4
            self.gap = (self.gap + 75) % (75*4)
        elif symbol == arcade.key.MOTION_UP or symbol == arcade.key.K:
            self.__index = (self.__index - 1) % 4
            self.gap = (self.gap - 75) % (75*4)
        elif symbol == arcade.key.ENTER:
            if self.__index != 3:
                self.window.show_view(self.menu_list[self.__index])
            else:
                exit(0)

    def draw_text_in_rect(
            self,
            x,
            y,
            width,
            height,
            color,
            text,
            font
            ):
        banner = arcade.XYWH(x, y, width, height)
        arcade.draw_rect_filled(banner, color)
        arcade.draw_text(text, x, y, arcade.color.YELLOW_ORANGE, font, anchor_x="center", anchor_y="center")

    def draw_menu(self):
        # DARK_BLUE
        arcade.draw_rect_filled(
            arcade.XYWH(self.width//2, (self.height // 2), 450, 700),
            arcade.color.DARK_BLUE
        )
        arcade.draw_rect_filled(
            arcade.XYWH(self.width//2, (self.height // 2) + 200, 370, 120),
            arcade.color.INDIAN_YELLOW
        )
        self.draw_text_in_rect(
            self.width//2,
            (self.height // 2) + 200,
            300,
            70,
            arcade.color.YELLOW,
            "PAC-MAN",
            30
            )

        arcade.draw_text(
                    "Start Game",
                    self.width // 2,
                    (self.height // 2),
                    arcade.color.WHITE,
                    20,
                    anchor_x="center",
                    anchor_y="center"
                )
        arcade.draw_text(
                    "View Highscores",
                    self.width // 2,
                    (self.height // 2) - 75,
                    arcade.color.WHITE,
                    20,
                    anchor_x="center",
                    anchor_y="center"
                )

        arcade.draw_text(
                    "Instructions",
                    self.width // 2,
                    (self.height // 2) - 150,
                    arcade.color.WHITE,
                    20,
                    anchor_x="center",
                    anchor_y="center"
                )
        arcade.draw_text(
                    "Exit",
                    self.width // 2,
                    (self.height // 2) - 225,
                    arcade.color.WHITE,
                    20,
                    anchor_x="center",
                    anchor_y="center"
                )
        arcade.draw_triangle_filled(
            (self.width/2) - 180, (self.height/2) + 10 - self.gap,
            (self.width/2) - 180, (self.height/2) - 10 - self.gap,
            (self.width/2) - 150, (self.height/2) - self.gap,
            arcade.color.WHITE
            )
