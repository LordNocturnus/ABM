from collections import abc
import math
import numpy as np  # type: ignore
import time as timer
import warnings

import constraints
from single_agent_planner_v2 import compute_heuristics, a_star, get_sum_of_cost, get_location
import base_solver


class PrioritizedPlanningSolver(base_solver.BaseSolver):
    """A planner that plans for each robot sequentially."""

    def __init__(self,
                 my_map: list[list[bool]],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int] = get_sum_of_cost,
                 heuristics_func: abc.Callable[
                     [list[list[bool]], tuple[int, int]],
                     dict[tuple[int, int], int]] = compute_heuristics,
                 printing: bool = True,
                 recursive: bool = True,
                 **kwargs) -> None:
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """
        super().__init__(my_map, starts, goals, score_func, heuristics_func, printing)
        self.recursive = recursive

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()

        result = self.solve_prioritized(base_constraints)

        self.CPU_time = timer.time() - start_time
        return result

    def solve_prioritized(self,
                          base_constraints: list[constraints.Constraint],
                          depth: int = 0) -> list[list[tuple[int, int]]]:
        result = []
        constraint_list: list[constraints.Constraint] = [*base_constraints]
        if depth == math.factorial(len(self.starts)):
            raise RecursionError('No solutions')

        for a, start in enumerate(self.starts):  # Find path for each agent
            path = a_star(self.my_map, start, self.goals[a], self.heuristics[a],
                          a, constraint_list)
            if path is None and a == 0:
                raise BaseException('No solutions')
            if path is None:
                self.starts[a], self.starts[a - 1] = self.starts[a - 1], self.starts[a]
                self.goals[a], self.goals[a - 1] = self.goals[a - 1], self.goals[a]
                self.heuristics[a], self.heuristics[a - 1] = self.heuristics[a - 1], self.heuristics[a]
                return self.solve_prioritized(base_constraints, depth + 1)
            result.append(path)

            for t, path_vertex in enumerate(path[:-1]):
                constraint_list.append(constraints.Constraint(True, a, t + 1, path_vertex, path[t + 1]))
            constraint_list.append(constraints.Constraint(True, a, len(path), path[-1], infinite=True))
        return result
