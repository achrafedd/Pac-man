*This project has been created as part of the 42 curriculum by niboutta, aeddiba.*

# Pac-Man

## Description

Pac-Man is a Python implementation of the classic arcade game. The player
guides Pac-Man through generated mazes, eats pacgums and power pellets,
avoids or hunts ghosts, and progresses through ten configured levels.

The game includes a graphical menu, gameplay HUD, pause screen, instructions,
highscore board, victory screen, and game-over screen. It is built with
object-oriented Python and the Arcade graphics library.

## Requirements

- Python 3.10 or newer
- `uv` (recommended) or another Python package manager
- The dependencies listed in `pyproject.toml`
- The assigned `mazegenerator` package

## Installation and Instructions

Install the dependencies with:

```bash
make install
```

Launch the game with exactly one JSON configuration file argument:

```bash
python3 pac-man.py config.json
```

The recommended project command is:

```bash
make run
```

Other Makefile commands are:

| Command | Purpose |
| --- | --- |
| `make install` | Install or synchronize dependencies with `uv` |
| `make run` | Start the game with `config.json` |
| `make lint` | Run Flake8 and mypy checks |
| `make clean` | Remove Python caches and mypy artifacts |
| `bash package.sh` | Build a PyInstaller distribution archive |

### Controls

- **Main menu:** use `J`/`K` or the menu navigation keys to select an item;
  press `Enter` to confirm and `Q` to quit.
- **Gameplay:** use the arrow keys to move.
- **Pause:** press `Escape`; choose resume or return to the main menu.
- **Cheat mode:** press `C` during gameplay to activate the evaluation
  helpers, and `N` to skip the current level.
- **Leaderboards and instructions:** press `M` to return to the main menu and
  `Q` to quit where supported.

## Configuration

The configuration file is JSON and may contain comment lines beginning with
`#`. Unknown keys are ignored by the configuration model. The supplied
`config.json` uses the following keys:

| Key | Type | Default | Description |
| --- | --- | ---: | --- |
| `highscore_filename` | string | `"leaderboard.json"` | JSON file used for persistent scores |
| `levels` | list of objects | `[{"width": 42, "height": 42}]` | Maze dimensions for each level |
| `lives` | integer | `3` | Number of lives at the start of a game |
| `points_per_pacgum` | integer | `10` | Points for eating a normal pacgum |
| `points_per_super_pacgum` | integer | `50` | Points for eating a power pellet |
| `points_per_ghost` | integer | `200` | Points for eating an edible ghost |
| `level_max_time` | integer | `90` | Time limit for a level, in seconds |
| `seed` | integer | `42` | Seed used when creating the mazes |

Each entry in `levels` must contain `width` and `height`. The supplied game
configuration contains ten levels, with dimensions between 10x10 and 30x20.
Invalid configuration values are reported as validation errors rather than
being allowed to start the game.

## Highscore

Scores are stored in the JSON file named by `highscore_filename`; the default
is `leaderboard.json`. A score is saved after a victory or game over. Player
names are limited to ten characters and scores must be non-negative integers.
The leaderboard is sorted from highest to lowest score and displays the top
ten entries from the main menu. Missing or malformed leaderboard files are
handled as an empty leaderboard.

## Maze Generation

The game uses the assigned external `mazegenerator` (A-Maze-ing) package
instead of implementing its own maze-generation algorithm. `components/Maze.py`
adapts the generated grid for Pac-Man, initializes pacgums, converts grid
coordinates to screen coordinates, and renders walls and corridors. The
configured seed is used for reproducible maze creation.

## Implementation

- **Language:** Python 3.10+
- **Graphics:** Arcade
- **Validation:** Pydantic configuration and leaderboard models
- **Maze generation:** external `mazegenerator` package
- **Persistence:** JSON configuration and highscore files
- **Packaging:** PyInstaller through `package.sh`
- **Quality checks:** Flake8 and mypy through the Makefile

The game loop is:

```text
Main menu -> start game -> win or lose -> enter name -> main menu
```

During a game, the player moves through corridors, eats pacgums and power
pellets, survives autonomous ghosts, and retains score and remaining lives
while advancing through levels. The HUD displays score, lives, level, and
remaining time.

## General Software Architecture

`pac-man.py` is the application entry point and owns the Arcade window and
high-level screen state. The `components` package contains the main
responsibilities:

- `Parser` reads the command-line argument, loads JSON with comments, and
  validates the configuration.
- `Config` and `LeaderBoardSchema` define validated application data.
- `Maze` manages generated grids, pacgums, screen coordinates, and rendering.
- `Player` manages Pac-Man movement, collision checks, and drawing.
- `Ghost` is the base class for ghost behavior; the red, pink, orange, and
  blue subclasses implement their movement strategies.
- `GameView` coordinates a level, collisions, scoring, timing, and the HUD.
- `MainMenu`, `PauseMenu`, `Instructions`, `LeaderBoard`, `GameOver`, and
  `Victory` implement the individual screens.
- `Stats` provides the screen-state values used by the main window.

## Project Management

The repository is organized around the source package, assets, configuration,
packaging script, and Makefile. The project was developed iteratively by
implementing the game loop, configuration parser, maze integration, gameplay
entities, screens, persistence, and packaging, then checking the code with
linting and static typing tools.

## Resources and AI Usage

### Resources

- [Python documentation](https://docs.python.org/3/)
- [Arcade documentation](https://api.arcade.academy/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [Python `json` module](https://docs.python.org/3/library/json.html)
- [PyInstaller documentation](https://pyinstaller.org/en/stable/)
- The supplied A-Maze-ing / `mazegenerator` package

### AI usage

AI tools were used as development assistance for repetitive documentation
work,
