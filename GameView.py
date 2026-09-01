import arcade

from Ghost import Ghost
from Maze import Maze
from Player import Direction, Player


class GameView(arcade.View):
    def __init__(self, maze: Maze) -> None:
        super().__init__()
        self.maze: Maze = maze
        self.player: Player = Player((0, 0), maze, size=30)
        self.ghost_red: Ghost = Ghost(10, 10, maze, arcade.color.RED)
        self.ghost_blue: Ghost = Ghost(0, 5, maze, arcade.color.CYAN)
        self.ghost_pink: Ghost = Ghost(13, 0, maze, arcade.color.PINK)
        self.ghost_orange: Ghost = Ghost(7, 9, maze, arcade.color.ORANGE)


    def on_draw(self) -> None:
        self.clear()
        self.maze.draw(self.width, self.height)
        self.player.draw()
        self.ghost_red.draw()
        self.ghost_blue.draw()
        self.ghost_pink.draw()
        self.ghost_orange.draw()

    def on_update(self, delta_time: float) -> None:
        self.player.d += 5 * delta_time
        self.player.move()

    def can_turn(self, x, y, dir):
        mask, _, _, _, _ = self.player.directions[dir.value]
        return not self.maze.maze[y][x] & mask

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.Q:
            self.window.close()
        # Controle directions of player
        if symbol == arcade.key.UP:
            if self.can_turn(self.player.x, self.player.y, Direction.UP):
                self.player.direction = Direction.UP
        if symbol == arcade.key.RIGHT:
            if self.can_turn(self.player.x, self.player.y, Direction.RIGHT):
                self.player.direction = Direction.RIGHT
        if symbol == arcade.key.DOWN:
            if self.can_turn(self.player.x, self.player.y, Direction.DOWN):
                self.player.direction = Direction.DOWN
        if symbol == arcade.key.LEFT:
            if self.can_turn(self.player.x, self.player.y, Direction.LEFT):
                self.player.direction = Direction.LEFT


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
        if symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.MOTION_DOWN or symbol == arcade.key.J:
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
