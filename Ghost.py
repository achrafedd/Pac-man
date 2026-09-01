import arcade
from arcade.types import Color

from Maze import Maze


class Ghost:
    def __init__(self, x: int, y: int, maze: Maze, color: Color) -> None:
        self.x: int = x
        self.y: int = y
        self.color: Color = color
        self.fear: bool = False
        self.maze: Maze = maze
        self.size: float = maze.size - 15

    def draw(self):
        if self.fear:
            self.color = arcade.color.BLUE
        x, y = self.maze.grid_to_pixel(self.x, self.y, self.maze.size)

        # Draw Body
        arcade.draw_arc_filled(x, y, self.size, self.size, self.color, 0, 180)
        height = self.size * 0.6
        body = arcade.XYWH(x, y - height // 2, self.size, height)
        arcade.draw_rect_filled(body, self.color)

        # Draw ayse yarbi tkon katkteb haka xD
        ayse_size = self.size * 0.2
        black_size = self.size * 0.1
        ayse_gap = self.size * 0.25
        if self.fear:
            arcade.draw_circle_filled(x + ayse_gap, y, ayse_size, (255, 255, 0))
            arcade.draw_circle_filled(x - ayse_gap, y, ayse_size, (255, 255, 0))
        else:
            arcade.draw_circle_filled(x + ayse_gap, y, ayse_size, (255, 255, 255))
            arcade.draw_circle_filled(x + ayse_gap, y, black_size, (0, 0, 0))
            arcade.draw_circle_filled(x - ayse_gap, y, ayse_size, (255, 255, 255))
            arcade.draw_circle_filled(x - ayse_gap, y, black_size, (0, 0, 0))

        # Draw mouth
        if self.fear:
            arcade.draw_arc_outline(x - 10, y - ayse_gap, 10, 10, (255, 255, 255), 0, 180)
            arcade.draw_arc_outline(x, y - ayse_gap, 10, 10, (255, 255, 255), 0, 180)
            arcade.draw_arc_outline(x + 10, y - ayse_gap, 10, 10, (255, 255, 255), 0, 180)

        # Draw leges
        leg_width = self.size // 3
        arcade.draw_arc_filled(x - leg_width, y - height + 1, leg_width, leg_width, self.color, 180, 360)
        arcade.draw_arc_filled(x, y - height + 1, leg_width, leg_width, self.color, 180, 360)
        arcade.draw_arc_filled(x + leg_width, y - height + 1, leg_width, leg_width, self.color, 180, 360)


# if __name__ == '__main__':
#     window = arcade.Window(fullscreen=True)
#     ghost = Ghost((255, 0, 0), window)
#     arcade.start_render()
#     ghost.draw()
#     arcade.finish_render()
#     arcade.run()
