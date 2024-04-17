from collections import abc
import time as timer

from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost
import base_solver
import constraints


class IndependentSolver(base_solver.BaseSolver):
    """
        A planner that plans for each robot independently. The class inherits from base_solver.BaseSolver for its basic
        functionality.

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

        :param printing:        {bool}      Vriable to enable and disable prtining within the model. This allows for the 
                                            user to specify if they would like to receive the solver outcome after every 
                                            run or not. True enables printing while false disables this behaviour. 
        """

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """ 
            Finds paths for all agents from their start locations to their goal locations. Overwrites the baseclass
            find_solution function.

        :param base_constraints:    {list}          Constraints to be condisdered during the solve procedure

        :return:                    {list}          Returns the paths traversed by all agents
        
        :raise:                     {BaseException} Raises a base exption, when no solution can be found for 
                                                    the specified scenario.
        """

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
