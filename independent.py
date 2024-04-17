from collections import abc
import time as timer

from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost
import base_solver
import constraints


class IndependentSolver(base_solver.BaseSolver):
    """A planner that plans for each robot independently."""

    def __init__(self,
                 my_map: list[list[bool]],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int] = get_sum_of_cost,
                 heuristics_func: abc.Callable[
                     [list[list[bool]], tuple[int, int]],
                     dict[tuple[int, int], int]] = compute_heuristics,
                 printing: bool = True,
                 **kwargs) -> None:
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """
        super().__init__(my_map, starts, goals, score_func, heuristics_func, printing)

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = []

        ##############################
        # Task 0: Understand the following code (see the lab description for some hints)

        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, base_constraints)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)

        ##############################

        self.CPU_time = timer.time() - start_time
        if self.printing:
            print("\n Found a solution! \n")
            print("CPU time (s):    {:.2f}".format(self.CPU_time))
            print("Sum of costs:    {}".format(get_sum_of_cost(result)))

        return result
