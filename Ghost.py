import arcade
from arcade.types import Color
from abc import ABC, abstractmethod
from Maze import Maze


class Ghost(ABC):
    def __init__(self, cordinates: tuple[int, int], maze: Maze, color: Color, player) -> None:
        self.x: int = cordinates[0]
        self.y: int = cordinates[1]
        self.color: Color = color
        self.fear: bool = False
        self.maze: Maze = maze
        self.size: float = maze.size // 2
        self.player = player

    @abstractmethod
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

    @abstractmethod
    def move(self) -> None:
        
        pass


class Red_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(self.x, self.y, maze.size)
        self.target_x, self.target_y = self.pixel_x, self.pixel_y
        self.move()

    def draw(self):
        return super().draw()

    def get_path(self):
        x_player = self.player.x
        y_player = self.player.y
        x_ghost = self.x
        y_ghost = self.y
        start = (x_ghost, y_ghost)
        goal = (x_player, y_player)
        queue = [start]
        visited = {start}
        parent = {}
        while queue:
            curr = queue.pop(0)
            if curr == goal:
                break
            x, y = curr
            for neighbor in self.maze.get_neighbor(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)
        path = []
        curr = goal
        while curr != start:
            path.append(curr)
            curr = parent[curr]
        path.append(start)
        path.reverse()
        return path

    def move(self):
        path = self.get_path()


    def update(self, delta_time: float) -> None:
        if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
            self.move()




class Pink_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)

    def draw(self):
        return super().draw()

    def move(self):
        return super().move()

class Orange_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)

    def draw(self):
        return super().draw()

    def move(self):
        return super().move()

class Blue_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)

    def draw(self):
        return super().draw()

    def move(self):
        return super().move()
