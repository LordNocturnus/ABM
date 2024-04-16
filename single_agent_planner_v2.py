import typing
from collections import abc
import heapq

import constraints
import utils


def move(loc: tuple[int, int], dir_idx: int) -> tuple[int, int]:
    return loc[0] + utils.DIRECTIONS[dir_idx][0], loc[1] + utils.DIRECTIONS[dir_idx][1]


def get_sum_of_cost(paths: list[list[tuple[int, int]]]) -> int:
    return sum([len(p) - 1 for p in paths])


def compute_heuristics(my_map: list[list[bool]], goal: tuple[int, int]) -> dict[tuple[int, int], int]:
    # Use Dijkstra to build a shortest-path tree rooted at the goal location
    open_list: list[tuple[int, tuple[int, int]]] = []
    closed_list = dict()
    heapq.heappush(open_list, (0, goal))
    closed_list[goal] = 0
    while len(open_list) > 0:
        (cost, loc) = heapq.heappop(open_list)
        child_cost = cost + 1
        for dir_idx in range(4):
            child_loc = move(loc, dir_idx)
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
                continue
            if my_map[child_loc[0]][child_loc[1]]:
                continue
            if child_loc in closed_list:
                existing_node_cost = closed_list[child_loc]
                if existing_node_cost > child_cost:
                    closed_list[child_loc] = child_cost
                    heapq.heappush(open_list, (child_cost, child_loc))
            else:
                closed_list[child_loc] = child_cost
                heapq.heappush(open_list, (child_cost, child_loc))

    # build the heuristics table
    return closed_list


def get_location(path: list[tuple[int, int]], time: int) -> tuple[int, int]:
    try:
        return path[time]
    except IndexError:
        return path[-1]


def a_star(my_map: list[list[bool]],
           start_loc: tuple[int, int],
           goal_loc: tuple[int, int],
           h_values: dict[tuple[int, int], int],
           agent: int,
           constraint_list: list[constraints.Constraint]) -> typing.Optional[list[tuple[int, int]]]:
    """ my_map      - binary obstacle map
        start_loc   - start position
        goal_loc    - goal position
        agent       - the agent that is being re-planned
        constraints - constraints defining where robot should or cannot go at each timestep
    """

    constraint_table = constraints.ConstraintTable(constraint_list, agent)
    open_list: list["AStarNode"] = []
    closed_list = dict()
    infinite_g_val = dict()
    earliest_goal_timestep = 0

    root = AStarNode(start_loc, 0, h_values[start_loc], 0)
    heapq.heappush(open_list, root)
    closed_list[(root.loc, root.step)] = root
    while len(open_list) > 0:
        curr = heapq.heappop(open_list)

        if curr.loc == goal_loc and curr.step >= earliest_goal_timestep:
            found = True
            if curr.step + 1 < len(constraint_table):
                for t in range(curr.step + 1, len(constraint_table)):
                    if constraint_table.is_constrained(goal_loc, goal_loc, t):
                        found = False
                        earliest_goal_timestep = t + 1
                        break
            if found:
                return curr.get_path()

        if constraint_table.is_infinite and curr.step + 1 >= len(constraint_table):
            if curr.loc in infinite_g_val and infinite_g_val[curr.loc] <= curr.g_val:
                continue
            infinite_g_val[curr.loc] = curr.g_val

        for dir_idx in range(5):
            child_loc = move(curr.loc, dir_idx)
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) \
               or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
               continue
            if my_map[child_loc[0]][child_loc[1]]:
                continue
            if constraint_table.is_constrained(curr.loc, child_loc, curr.step + 1):
                continue
            child = AStarNode(child_loc, curr.g_val + 1, h_values[child_loc], curr.step + 1, curr)
            if (child.loc, child.step) in closed_list:
                existing_node = closed_list[(child.loc, child.step)]
                if child < existing_node:
                    closed_list[(child.loc, child.step)] = child
                    heapq.heappush(open_list, child)
            else:
                closed_list[(child.loc, child.step)] = child
                heapq.heappush(open_list, child)

    return None  # Failed to find solutions


class AStarNode:

    def __init__(self,
                 loc: tuple[int, int],
                 g_val: float,
                 h_val: float,
                 step: int,
                 parent: typing.Optional["AStarNode"] = None) -> None:
        self.loc = loc
        self.g_val = g_val
        self.h_val = h_val
        self.score = g_val + h_val
        self.step = step
        self.parent = parent

    def get_path(self) -> list[tuple[int, int]]:
        if self.parent:
            return self.parent.get_path() + [self.loc]
        else:
            return [self.loc]

    def __lt__(self, other: "AStarNode") -> bool:
        """Return true is "self" is better than "other"."""
        if self.score == other.score:
            if self.h_val == other.h_val:
                if self.loc[0] == other.loc[0]:
                    if self.loc[1] == other.loc[1]:
                        return False
                    return self.loc[1] < other.loc[1]
                return self.loc[0] < other.loc[0]
            return self.h_val < other.h_val
        return self.score < other.score
