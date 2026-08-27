import arcade


class Player:
    def __init__(self,
                 cordinates: tuple[int, int],
                 direction: str = 'right',
                 size: int = 10
                 ) -> None:
        self.cordinates: tuple[int, int] = cordinates
        self.direction: str = direction
        self.size: int = size
        self.directions: dict[str, tuple[int, int]] = {
                'right': (30, 330),
                'down': (300, 600),
                'left': (210, 510),
                'up': (120, 420)
                }

    def draw(self) -> None:
        cx, cy = self.cordinates
        se, ee = self.directions[self.direction]
        arcade.draw_arc_filled(cx,
                               cy,
                               self.size,
                               self.size,
                               arcade.color.YELLOW,
                               se,
                               ee)

    def move(self) -> None:
        pass
