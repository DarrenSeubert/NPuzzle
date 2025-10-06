# NPuzzle

This program solves the N-Puzzle (sliding tile puzzle) using the A* search algorithm with Manhattan Distance as the heuristic and tree pruning. It supports both manual and random puzzle generation, checks for solvability. It then prints the solution path with move numbers, heuristic values, and statistics like total number of moves and maximum queue length.

https://github.com/user-attachments/assets/85564058-331b-47f3-931c-0b655f4d6957

## Program Operation Overview

- Prompts the user for the grid size (e.g., 3 for a 3x3 puzzle).
- Allows manual entry of puzzle tiles or generates a random puzzle.
- Checks if the puzzle is solvable (unless the unsolvable mode is enabled).
- If solvable, finds the shortest solution path using A* and prints each move.

## Command-Line Flags

- -m or --manual: Enables manual mode for puzzle entry. You will be prompted to enter each tile value.
- -u or --unsolvable: Allows the program to generate or accept unsolvable puzzles. By default, only solvable puzzles are accepted/generated.

## Future Extensions

- Implement Walking Distance Heuristic
- Implement Lower Bound Pruning

## Useful Links

- [How to create an automatic puzzle solving program](https://computerpuzzle.net/puzzle/15puzzle/index.html)
- [About Walking Distance](https://computerpuzzle.net/english/15puzzle/wd.gif)
- [Iterative deepening A*](https://en.wikipedia.org/wiki/Iterative_deepening_A*)
- [Solve the 15 Puzzle (the tile-sliding puzzle)](https://codegolf.stackexchange.com/questions/6884/solve-the-15-puzzle-the-tile-sliding-puzzle)
- [Cache is King](https://newscrewdriver.com/2016/06/19/cache-is-king/)
- [How to check if an instance of 15 puzzle is solvable?](https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/)
