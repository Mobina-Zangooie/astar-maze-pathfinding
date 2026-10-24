"""A* search on a 5x5 maze with a bridge and a river.

The maze is stored as an 11x11 grid: the cells of the 5x5 maze sit at odd
coordinates, and the entries between them are walls (0) or openings (1).
The grid is converted to a graph of 5x5 cells, so every move goes from one
cell to a neighboring cell and the printed path and cost are in 5x5 terms.
"""

import heapq
import itertools
from math import inf

# --- Problem data -----------------------------------------------------------

# 0 = wall, 1 = open
MAZE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
SIZE = 5  # the maze has 5x5 cells

START = (0, 0)  # (row, column) in 5x5 coordinates
GOAL = (0, 3)

STEP_COST = 1    # cost of a normal move
BRIDGE_COST = 4  # cost of crossing the bridge (replaces the normal cost)
RIVER_COST = 2   # cost of crossing the river (replaces the normal cost)

# Moves that cost something special: the pair of cells the move connects.
SPECIAL_MOVES = {
    frozenset({(1, 2), (1, 3)}): BRIDGE_COST,
    frozenset({(1, 4), (2, 4)}): RIVER_COST,
}

# Priority order when costs are equal: left, down, right, up
MOVES = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# --- Graph ------------------------------------------------------------------

def neighbors(cell):
    """Yield (neighbor, move_cost) for every cell reachable in one move."""
    row, col = cell
    for d_row, d_col in MOVES:
        n_row, n_col = row + d_row, col + d_col
        if not (0 <= n_row < SIZE and 0 <= n_col < SIZE):
            continue
        # The entry of the 11x11 grid between the two cells is the wall slot
        if MAZE[2 * row + 1 + d_row][2 * col + 1 + d_col] == 0:
            continue
        neighbor = (n_row, n_col)
        cost = SPECIAL_MOVES.get(frozenset({cell, neighbor}), STEP_COST)
        yield neighbor, cost


def heuristic(a, b):
    """Manhattan distance, scaled by the cheapest possible move.

    Scaling keeps the heuristic admissible even if a special move is cheaper
    than a normal one.
    """
    cheapest = min(STEP_COST, *SPECIAL_MOVES.values())
    return cheapest * (abs(a[0] - b[0]) + abs(a[1] - b[1]))


# --- A* ---------------------------------------------------------------------

def a_star(start, goal):
    """Return (path, total_cost, expanded_cells).

    expanded_cells are the cells taken out of the open list, in order.
    path is None and total_cost is inf if the goal cannot be reached.
    """
    counter = itertools.count()  # equal f: the earlier inserted cell goes first
    open_heap = [(heuristic(start, goal), next(counter), start)]
    g_score = {start: 0}
    came_from = {}
    closed = set()
    expanded = []

    while open_heap:
        _, _, current = heapq.heappop(open_heap)
        if current in closed:  # outdated duplicate entry
            continue
        closed.add(current)
        expanded.append(current)

        if current == goal:
            return build_path(came_from, current), g_score[current], expanded

        for neighbor, cost in neighbors(current):
            new_g = g_score[current] + cost
            if new_g < g_score.get(neighbor, inf):
                g_score[neighbor] = new_g
                came_from[neighbor] = current
                f_score = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score, next(counter), neighbor))

    return None, inf, expanded


def build_path(came_from, current):
    """Walk back from the goal to the start."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def main():
    path, total_cost, expanded = a_star(START, GOAL)
    if path is None:
        print("No path found")
        return
    print("Path:", path)
    print("Expanded cells (in order):", expanded)
    print("Total cost:", total_cost)


if __name__ == "__main__":
    main()
