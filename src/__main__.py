from mazegenerator import MazeGenerator


def main() -> None:
    size = (42, 42)
    maze = MazeGenerator(size, False)
    maze.generate(42)
    grids = maze.maze
    print(grids)


if __name__ == "__main__":
    main()
