import typing
from collections import abc
import numba as nb
import numpy as np
import numpy.typing as npt
import heapq

import constraints_v2
import utils


#@nb.jit(nopython=True)  # type: ignore
def move(loc: npt.NDArray[int], dir_idx: int) -> npt.NDArray[int]:
    return loc + utils.DIRECTIONS[dir_idx]


#@nb.jit(nopython=True)  # type: ignore
def get_sum_of_cost(paths: list[list[npt.NDArray[int]]]) -> int:
    return sum([len(p) - 1 for p in paths])


#@nb.jit(nopython=True)  # type: ignore
def compute_heuristics(my_map: npt.NDArray[bool], goal: npt.NDArray[int]) -> npt.NDArray[int]:
    # Use Dijkstra to build a shortest-path tree rooted at the goal location
    open_list: list[DijkstraNode] = []
    closed_list = np.full_like(my_map, my_map.shape[0] * my_map.shape[1])
    heapq.heappush(open_list, DijkstraNode(0, goal))
    closed_list[*goal] = 0

    while len(open_list) > 0:
        curr = heapq.heappop(open_list)
        child_cost = curr.cost + 1
        for dir_idx in range(4):
            child_loc = move(curr.loc, dir_idx)
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
                continue
            if my_map[*child_loc]:
                continue
            existing_node_cost = closed_list[*child_loc]
            if existing_node_cost > child_cost:
                closed_list[child_loc] = child_cost
                heapq.heappush(open_list, DijkstraNode(child_cost, child_loc))

    # build the heuristics table
    return closed_list


#@nb.jit(nopython=True)  # type: ignore
def get_location(path: list[npt.NDArray[int]], time: int) -> npt.NDArray[int]:
    try:
        return path[time]
    except IndexError:
        return path[-1]


#@nb.jit(nopython=True)  # type: ignore
def a_star(my_map: list[list[bool]],
           start_loc: npt.NDArray[int],
           goal_loc: npt.NDArray[int],
           h_values: npt.NDArray[int],
           agent: int,
           constraint_list: list[constraints_v2.Constraint]) -> typing.Optional[list[npt.NDArray[int]]]:
    """ my_map      - binary obstacle map
        start_loc   - start position
        goal_loc    - goal position
        agent       - the agent that is being re-planned
        constraints - constraints defining where robot should or cannot go at each timestep
    """

    constraint_table = constraints_v2.ConstraintTable(constraint_list, agent)
    open_list: list["AStarNode"] = []
    closed_list = dict()
    earliest_goal_timestep = 0
    root = AStarNode(start_loc, 0, h_values[*start_loc], 0)
    heapq.heappush(open_list, root)
    closed_list[(*root.loc, root.step)] = root
    while len(open_list) > 0:
        curr = heapq.heappop(open_list)
        if np.all(curr.loc - goal_loc == 0) and curr.step >= earliest_goal_timestep:
            found = True
            if curr.step + 1 < len(constraint_table):
                for t in range(curr.step + 1, len(constraint_table)):
                    if constraint_table.is_constrained(goal_loc, goal_loc, t):
                        found = False
                        earliest_goal_timestep = t + 1
                        break
            if found:
                return curr.get_path()
        for dir_idx in range(5):
            child_loc = move(curr.loc, dir_idx)
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) \
               or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
               continue
            if my_map[child_loc[0]][child_loc[1]]:
                continue
            if constraint_table.is_constrained(curr.loc, child_loc, curr.step + 1):
                continue
            child = AStarNode(child_loc, curr.g_val + 1, h_values[*child_loc], curr.step + 1, curr)
            if (*child.loc, child.step) in closed_list:
                existing_node = closed_list[(*child.loc, child.step)]
                if child < existing_node:
                    closed_list[(*child.loc, child.step)] = child
                    heapq.heappush(open_list, child)
            else:
                closed_list[(*child.loc, child.step)] = child
                heapq.heappush(open_list, child)

    return None  # Failed to find solutions


class DijkstraNode:

    def __init__(self,
                 cost: int,
                 loc: npt.NDArray[int]) -> None:
        self.cost = cost
        self.loc = loc

    def __lt__(self, other: "DijkstraNode") -> bool:
        """Return true is "self" is better than "other"."""
        if self.cost == other.cost:
            if self.loc[0] == other.loc[0]:
                if self.loc[1] == other.loc[1]:
                    return False
                return self.loc[1] < other.loc[1]
            return self.loc[0] < other.loc[0]
        return self.cost < other.cost


class AStarNode:

    def __init__(self,
                 loc: npt.NDArray[int],
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

    def get_path(self) -> list[npt.NDArray[int]]:
        if self.parent:
            ret = self.parent.get_path()
            ret.append(self.loc)
            return ret
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
