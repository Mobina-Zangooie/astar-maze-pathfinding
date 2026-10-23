# A* Maze Pathfinding

A Python implementation of the A* search algorithm for finding a path through a maze. This project was developed as an AI course assignment.

## Problem

Find a path from the start cell to the goal cell in a maze. Cells marked 0 are walls and cells marked 1 are traversable. Movement is allowed in four directions: up, down, left, and right.

The maze is encoded directly in A-Star-Algorithm.py as an 11 × 11 list. The start coordinate is (1, 1) and the goal coordinate is (1, 7), using zero-based (row, column) coordinates.

## Inputs

The algorithm receives:
- maze: a two-dimensional list where 0 means wall and 1 means walkable.
- start: the starting cell, (1, 1).
- goal: the target cell, (1, 7).
- bridge = 4 and river = 2: additional cost constants used by the code's special-transition checks.

The maze, start, goal, and cost constants are currently hard-coded in the Python file; the program does not ask the user for interactive input.

## Cost Function

The implementation starts each move with a base cost of 1. It then adds the configured bridge cost (4) or river cost (2) when the relevant coordinate checks match.

For a node n, A* uses:

- g(n): accumulated path cost from the start to n.
- h(n): estimated remaining cost from n to the goal.
- f(n) = g(n) + h(n): priority used to select the next node.

Implementation note: the special bridge/river checks are coordinate-specific and direction-specific in the current code. They should be reviewed before treating the result as a fully validated weighted-maze solution.

## Heuristic

The heuristic is Manhattan distance:

h(a, b) = abs(a.row - b.row) + abs(a.column - b.column)

This estimates the number of horizontal and vertical steps between two cells. It is commonly used for four-direction grid movement. For a weighted-cost problem, heuristic admissibility depends on the minimum possible cost per step and how the special costs are modeled.

## How to Run

Requirements: Python 3. No third-party packages are required; the code uses Python's standard-library heapq.

Run from the repository directory:

python A-Star-Algorithm.py
The script prints the converted 5 × 5 path and the filtered path cost.

## Example Result

Running the current implementation with its hard-coded maze returns this path in the original 11 × 11 coordinates:

(1,1) → (2,1) → (3,1) → (3,2) → (3,3) → (4,3) → (5,3) → (6,3) → (7,3) → (7,4) → (7,5) → (6,5) → (5,5) → (4,5) → (3,5) → (3,6) → (3,7) → (2,7) → (1,7)

The a_star() function returns a cost of 22 for that path. The script's final printed filtered-path cost is calculated separately after filtering the path and is 12; these are different calculations in the current code.

## Output Visualization

The image below visualizes the path returned by the current A* function on the original 11 × 11 maze.

![A* path output on the 11x11 maze](astar-maze-output.png)

## Files

- A-Star-Algorithm.py — A* implementation and hard-coded maze.
- problem.jpg — original problem illustration.
- astar-maze-output.png — visualization of the path returned by the current implementation.

## Project Status

Completed AI course project. The implementation and its cost-calculation details can be refined in a future version.
