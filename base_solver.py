import collections.abc as abc

import constraints


class BaseSolver:

    def __init__(self,
                 my_map: list[list[bool]],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int],
                 heuristics_func: abc.Callable[[list[list[bool]], tuple[int, int]], dict[tuple[int, int], int]],
                 printing: bool,
                 **kwargs) -> None:
        self.CPU_time: float = 0.0
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.score_func = score_func
        self.heuristics_func = heuristics_func
        self.printing = printing

        self.num_of_agents = len(goals)
        self.heuristics: list[dict[tuple[int, int], int]] = []

        # compute heuristics for the low-level search
        for goal in self.goals:
            self.heuristics.append(self.heuristics_func(my_map, goal))

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        raise NotImplementedError
