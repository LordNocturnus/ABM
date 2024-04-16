from collections import abc
import math
import numpy as np  # type: ignore
import time as timer
import warnings

import constraints
from single_agent_planner_v2 import compute_heuristics, a_star, get_sum_of_cost, get_location
import base_solver


class PrioritizedPlanningSolver(base_solver.BaseSolver):
    """
        A planner that plans for each robot sequentially. Meaning that first on robot is fully planned, afterwards the 
        next robot is planned keeping in mind the trajectory of the previous robot. The class inherits from 
        base_solver.BaseSolver for its basic functionality.
    
    :param CPU_time:        {float}     Value to keep track of the cpu time required for the solver to complete the 
                                        planning

    :param my_map:          {list}      List of list of boolean, discribing the map environment. The location of the 
                                        boolean value within the list disribes the location within its location within 
                                        the map.

    :param starts:          {list}      List of starting positions for the agents. Given as list of tuple of ineteger,
                                        where each each tuple is of the following form (y, x)
                                        [(x1, y1), (x2, y2), ...]

    :param goals:           {list}      List of goal/ end positions for the agents. Given as list of tuple of ineteger,
                                        where each each tuple is of the following form (y, x)
                                        [(x1, y1), (x2, y2), ...]

    :param printing:        {bool}      Vriable to enable and disable prtining within the model. This allows for the user 
                                        to specify if they would like to receive the solver outcome after every run or not.
                                        True enables printing while false disables this behaviour. 
    
    :param num_of_agents:   {int}       The number of agents within the environment. Extracted from the supplied goal or 
                                        start positions.
    
    :param heuritics:       {list}      List containing the heuristics.

    :param recursive:       {bool}      Boolean value enabling and disabling recursive mode (...)
    """

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
        super().__init__(my_map, starts, goals, score_func, heuristics_func, printing)
        """
            Initialise an instance of the BaseSolver class.

        :param my_map:          {list}      List of list of boolean, discribing the map environment. The location of the 
                                            boolean value within the list disribes the location within its location within 
                                            the map.

        :param starts:          {list}      List of starting positions for the agents. Given as list of tuple of ineteger,
                                            where each each tuple is of the following form (y, x).

        :param goals:           {list}      List of goal/end positions for the agents. Given as list of tuple of ineteger,
                                            where each each tuple is of the following form (y, x).

        :param score_func:      {function}  Score function 

        :param heuristics_func: {function}  Heuristics funtion

        :param printing:        {bool}      Variable to enable and disable prtining within the model. This allows for the 
                                            user to specify if they would like to receive the solver outcome after every 
                                            run or not. True enables printing while false disables this behaviour. 
        
        :param recursive:       {bool}      Boolean value enabling and disabling recursive mode (...) 
        """
        
        self.recursive = recursive

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """ 
            Finds paths for all agents from their start locations to their goal locations. Overwrites the baseclass
            find_solution function.

        :param base_constraints:    {list}          Constraints to be condisdered during the solve procedure

        :return:                    {list}          Returns the paths traversed by all agents
        """

        start_time = timer.time()

        result = self.solve_prioritized(base_constraints)

        self.CPU_time = timer.time() - start_time
        return result

    def solve_prioritized(self,
                          base_constraints: list[constraints.Constraint],
                          depth: int = 0) -> list[list[tuple[int, int]]]:
        """ 
            Finds paths for all agents from their start locations to their goal locations. Overwrites the baseclass
            find_solution function.

        :param base_constraints:    {list}              Constraints to be condisdered during the solve procedure

        :param depth:               {int}               How many recursion steps have been taken so far. Used to
                                                        ensure failure incase of infinite recursion.
        
        :return:                    {list}              Returns the paths traversed by all agents
        
        :raise:                     {BaseException}     Raises a base exption, when no solution can be found for 
                                                        the specified scenario.
        
        :raise:                     {RecursionError}    Raises a base exption, when no solution can be found for 
                                                        the specified scenario.
        """


        result = []
        constraint_list: list[constraints.Constraint] = [*base_constraints]
        # Escape infinite recursion
        if depth == math.factorial(len(self.starts)):
            raise RecursionError('No solutions')

        for a, start in enumerate(self.starts):  # Find path for each agent
            
            # Plan the path for agent a starting at start
            path = a_star(self.my_map, start, self.goals[a], self.heuristics[a],
                          a, constraint_list)
            
            # No solution found
            if path is None and (a == 0 or self.recursive == False):
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
