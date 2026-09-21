import arcade
from arcade.types import Color
from abc import ABC, abstractmethod
from .Maze import Maze
from .Player import Player


class Ghost(ABC):
    def __init__(
        self, cordinates: tuple[int, int], maze: Maze, color: Color, player
    ) -> None:
        self.x: int = cordinates[0]
        self.y: int = cordinates[1]
        self.color: Color = color
        self.fear: bool = False
        self.maze: Maze = maze
        self.size: float = maze.size // 2
        self.player: Player = player
        self.pixel_x, self.pixel_y = maze.grid_to_pixel(
            self.x, self.y, maze.size
        )
        self.target_x, self.target_y = self.pixel_x, self.pixel_y
        self.speed: int = 4

    @abstractmethod
    def _restart(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
            self.move()

        step = self.speed * self.maze.size * delta_time
        step /= 1.5
        dx = self.target_x - self.pixel_x
        dy = self.target_y - self.pixel_y
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= step or distance == 0:
            self.pixel_x = self.target_x
            self.pixel_y = self.target_y
        else:
            self.pixel_x += dx / distance * step
            self.pixel_y += dy / distance * step

    @abstractmethod
    def get_path(self):
        pass

    def draw(self):
        if self.fear:
            self.color = arcade.color.BLUE
        x, y = (self.pixel_x, self.pixel_y)

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
            arcade.draw_circle_filled(
                x + ayse_gap, y, ayse_size, (255, 255, 0)
            )
            arcade.draw_circle_filled(
                x - ayse_gap, y, ayse_size, (255, 255, 0)
            )
        else:
            arcade.draw_circle_filled(
                x + ayse_gap, y, ayse_size, (255, 255, 255)
            )
            arcade.draw_circle_filled(x + ayse_gap, y, black_size, (0, 0, 0))
            arcade.draw_circle_filled(
                x - ayse_gap, y, ayse_size, (255, 255, 255)
            )
            arcade.draw_circle_filled(x - ayse_gap, y, black_size, (0, 0, 0))

        # Draw mouth
        if self.fear:
            arcade.draw_arc_outline(
                x - 10, y - ayse_gap, 10, 10, (255, 255, 255), 0, 180
            )
            arcade.draw_arc_outline(
                x, y - ayse_gap, 10, 10, (255, 255, 255), 0, 180
            )
            arcade.draw_arc_outline(
                x + 10, y - ayse_gap, 10, 10, (255, 255, 255), 0, 180
            )

        # Draw leges
        leg_width = self.size // 3
        arcade.draw_arc_filled(
            x - leg_width,
            y - height + 1,
            leg_width,
            leg_width,
            self.color,
            180,
            360,
        )
        arcade.draw_arc_filled(
            x, y - height + 1, leg_width, leg_width, self.color, 180, 360
        )
        arcade.draw_arc_filled(
            x + leg_width,
            y - height + 1,
            leg_width,
            leg_width,
            self.color,
            180,
            360,
        )

    @abstractmethod
    def move(self) -> None:
        pass


class Red_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)

    def _restart(self) -> None:
        self.x, self.y = (0, 0)
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(
            0, 0, self.maze.size
        )
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def get_path(self):
        x_player = self.player.x
        y_player = self.player.y
        x_ghost = self.x
        y_ghost = self.y
        start = (y_ghost, x_ghost)
        goal = (y_player, x_player)
        queue = [start]
        visited = {start}
        parent = {}
        while queue:
            # print(queue)
            curr = queue.pop(0)
            if curr == goal:
                break
            y, x = curr
            for neighbor in self.maze.get_neighbor(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)
        path = []
        curr = goal
        while curr != start:
            path.append(curr)
            curr = parent.get(curr, None)
            if curr is None:
                return []
        path.append(start)
        path.reverse()
        return path

    def move(self):
        path = self.get_path()
        if len(path) < 2:
            return
        self.y, self.x = path[1]
        self.target_x, self.target_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )


class Pink_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)

    def _restart(self) -> None:
        self.x, self.y = (self.maze.width - 1, 0)
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def draw(self):
        return super().draw()

    def get_path(self):
        x_player = self.player.x
        y_player = self.player.y
        x_ghost = self.x
        y_ghost = self.y
        start = (y_ghost, x_ghost)
        # 1 right
        # 2 down
        # 3 left
        # 0 up
        if self.player.dir == 1:
            goal = (y_player, (x_player + 1) % (self.maze.width - 1))
        elif self.player.dir == 2:
            goal = ((y_player + 1) % (self.maze.height - 1), x_player)
        elif self.player.dir == 3:
            goal = (y_player, (x_player - 1) % (self.maze.width - 1))
        else:
            goal = ((y_player - 1) % (self.maze.height - 1), x_player)
        queue = [start]
        visited = {start}
        parent = {}
        while queue:
            curr = queue.pop(0)
            if curr == goal:
                break
            y, x = curr
            for neighbor in self.maze.get_neighbor(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)
        path = []
        curr = goal
        while curr != start:
            path.append(curr)
            curr = parent.get(curr, None)
            if curr is None:
                return []
        path.append(start)
        path.reverse()
        return path

    def move(self):
        path = self.get_path()
        if len(path) < 2:
            return
        self.y, self.x = path[1]
        self.target_x, self.target_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )


class Orange_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player):
        super().__init__(cordinates, maze, color, player)
        self.raduis = 5

    def _restart(self) -> None:
        self.x, self.y = (0, self.maze.height - 1)
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def draw(self):
        return super().draw()

    def get_path(self, goal):
        x_ghost = self.x
        y_ghost = self.y
        start = (y_ghost, x_ghost)
        queue = [start]
        visited = {start}
        parent = {}
        while queue:
            curr = queue.pop(0)
            if curr == goal:
                break
            y, x = curr
            for neighbor in self.maze.get_neighbor(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)
        path = []
        curr = goal
        while curr != start:
            path.append(curr)
            curr = parent.get(curr, None)
            if curr is None:
                return []
        path.append(start)
        path.reverse()
        return path

    def move(self):
        if (self.x - self.player.x) ** 2 + (
            self.y - self.player.y
        ) ** 2 <= self.raduis**2:
            home = self.get_path((self.maze.height - 1, 0))
            if len(home) < 2:
                return
            self.y, self.x = home[1]
        else:
            path = self.get_path((self.player.y, self.player.x))
            if len(path) < 2:
                return
            self.y, self.x = path[1]

        self.target_x, self.target_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )


class Blue_Ghost(Ghost):
    def __init__(self, cordinates, maze, color, player, red_ghost: Red_Ghost):
        super().__init__(cordinates, maze, color, player)
        self.red_ghost = red_ghost

    def _restart(self) -> None:
        self.x, self.y = (self.maze.height - 1, self.maze.height - 1)
        self.pixel_x, self.pixel_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )
        self.target_x, self.target_y = self.pixel_x, self.pixel_y

    def draw(self):
        return super().draw()

    def get_path(self, goal):
        x_ghost = self.x
        y_ghost = self.y
        start = (y_ghost, x_ghost)
        queue = [start]
        visited = {start}
        parent = {}
        while queue:
            curr = queue.pop(0)
            if curr == goal:
                break
            y, x = curr
            for neighbor in self.maze.get_neighbor(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)
        path = []
        curr = goal
        while curr != start:
            path.append(curr)
            curr = parent.get(curr, None)
            if curr is None:
                return []
        path.append(start)
        path.reverse()
        return path

    def move(self):
        if self.player.dir == 1:  # right
            ahead = (self.player.y, (self.player.x + 2) % self.maze.width)
        elif self.player.dir == 2:  # down
            ahead = ((self.player.y + 2) % self.maze.height, self.player.x)
        elif self.player.dir == 3:  # left
            ahead = (self.player.y, (self.player.x - 2) % self.maze.width)
        else:  # up
            ahead = ((self.player.y - 2) % self.maze.height, self.player.x)

        goal = (
            2 * ahead[0] - self.red_ghost.y,
            2 * ahead[1] - self.red_ghost.x,
        )

        goal = (
            max(0, min(self.maze.height - 1, goal[0])),
            max(0, min(self.maze.width - 1, goal[1])),
        )

        path = self.get_path(goal)
        if len(path) < 2:
            return

        self.y, self.x = path[1]
        self.target_x, self.target_y = self.maze.grid_to_pixel(
            self.x, self.y, self.maze.size
        )
