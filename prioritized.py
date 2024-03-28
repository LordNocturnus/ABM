import typing
import math
import numpy as np  # type: ignore
import time as timer

import constraints
from single_agent_planner_v2 import compute_heuristics, a_star, get_sum_of_cost, get_location
from constraints import Constraint

import warnings


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self,
                 my_map: list[list[bool]],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]]) -> None:
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.CPU_time: float = 0.0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self, recursive: bool = True) -> list[list[tuple[int, int]]]:
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = find_restricted_path(self.my_map, self.starts, self.goals, self.heuristics, recursive=recursive)


            ##############################
            # Task 2: Add constraint_list here
            #         Useful variables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraint_list: array of constraint_list to consider for future A* searches


            ##############################

        self.CPU_time = timer.time() - start_time

        #print("\n Found a solution! \n")
        #print("CPU time (s):    {:.2f}".format(self.CPU_time))
        #print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        #print(result)
        return result


def find_restricted_path(my_map: list[list[bool]],
                         starts: list[tuple[int, int]],
                         goals: list[tuple[int, int]],
                         heuristics: list[dict[tuple[int, int], int]],
                         depth: int = 0,
                         recursive: bool = True) -> list[list[tuple[int, int]]]:
    result = []
    constraint_list: list[constraints.Constraint] = []
    if depth == math.factorial(len(starts)):
        raise BaseException('No solutions')

    for a, start in enumerate(starts):  # Find path for each agent
        path = a_star(my_map, start, goals[a], heuristics[a],
                      a, constraint_list)
        if path is None:
            raise BaseException('No solutions')
        result.append(path)

        for t, path_vertex in enumerate(path):
            if t == len(path) - 1:
                for dt in range(20):
                    constraint_list.append(Constraint(True, a, t + dt, path_vertex, path[min(t + 1, len(path) - 1)]))
                    # constraint_list.append({'positive': True, 'agent': a, 'loc': [path[-1]], 'timestep': t + dt})#"""
            # constraint_list.append({'positive': True, 'agent': a, 'loc': [path_vertex, path[min(i+1, len(path)-1)]], 'timestep': i + 1})
            constraint_list.append(Constraint(True, a, t + 1, path_vertex, path[min(t + 1, len(path) - 1)]))

        if recursive:
            for a2, p in enumerate(result[:-1]):
                for t in range(max(len(path), len(p))):
                    if np.linalg.norm(np.asarray(get_location(p, t)) - np.asarray(get_location(path, t))) < 0.7:
                        with warnings.catch_warnings():
                            warnings.simplefilter("always")
                            warnings.warn(f"COLLISION ON DEPTH {depth}!!!")
                        starts[a], starts[a2] = starts[a2], starts[a]
                        goals[a], goals[a2] = goals[a2], goals[a]
                        heuristics[a], heuristics[a2] = heuristics[a2], heuristics[a]
                        return find_restricted_path(my_map, starts, goals, heuristics, depth + 1)
    return result
