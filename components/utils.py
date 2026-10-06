from pydantic import BaseModel, Field, model_validator
from enum import auto, Enum


class Stats(Enum):
    """Represent stats behavior.
    """
    MAIN_MENU = auto()
    LEADERBOARD = auto()
    GAME_VIEW = auto()
    INSTRUCTIONS = auto()
    PAUSE_MENU = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    EXIT = auto()


class Config(BaseModel):
    """Represent config behavior.
    """
    highscore_filename: str = "leaderboard.json"
    levels: list[dict[str, int]] = [{"width": 42, "height": 42}]
    lives: int = 3
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    level_max_time: int = 90
    seed: int = 42

    @model_validator(mode="after")
    def validate_filename(self) -> "Config":
        """Perform the validate filename operation.

        Returns:
            'Config': The operation result.
        """
        if not self.highscore_filename.endswith(".json"):
            raise ValueError("The highscore_filename must be JSON file")
        if self.highscore_filename.find("/") != -1:
            raise ValueError(
                (
                    "The highscore_filename must be"
                    " JSON file directories ar not allowd"
                )
            )
        if self.lives > 10:
            raise ValueError(
                f"The {self.lives} Lives is too much the max is 10"
            )
        if self.lives < 1:
            raise ValueError(
                f"The {self.lives} Lives is not allowd the min is 10"
            )
        if self.points_per_pacgum < 1:
            raise ValueError(
                f"The {self.lives} pacgum points is not allowd the min is 10"
            )
        if self.points_per_super_pacgum < 1:
            raise ValueError(
                (
                    f"The {self.lives} super pacgums points"
                    " Lives is not allowd the min is 10"
                )
            )
        if self.points_per_ghost < 1:
            raise ValueError(
                (
                    f"The {self.lives} ghosts points Lives"
                    " is not allowd the min is 10"
                )
            )
        if self.level_max_time < 90:
            raise ValueError(
                f"The minimum time is 90 {self.level_max_time} is invalid"
            )
        for level in self.levels:
            if level["width"] < 8 or level["height"] < 8:
                raise ValueError("The minimum height and width is 8")
            if level["width"] > 40 or level["height"] > 40:
                raise ValueError("The miximum height and width is 40")
        if len(self.levels) < 10:
            raise ValueError("The minimum levels is 10")

        return self


class LeaderBoardSchema(BaseModel):
    """Represent leaderboardschema behavior.
    """
    name: str = Field(..., max_length=10)
    score: int = Field(..., ge=0)
