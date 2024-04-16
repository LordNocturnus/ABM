import collections.abc as abc

import constraints


class BaseSolver:
    """
        Base Solver class used as a common basis point for the other solver classes (Independent, distibuted, cbs and 
        prioritized).

    :param CPU_time:        {float}     Value to keep track of the cpu time required for the solver to complete the 
                                        planning

    :param my_map:          {list}      List of list of boolean, discribing the map environment. The location of the 
                                        boolean value within the list disribes the location within its location within 
                                        the map.

    :param starts:          {list}      List of starting positions for the agents. Given as list of tuple of ineteger,
                                        where each each tuple is of the following form (y, x)

    :param goals:           {list}      List of goal/ end positions for the agents. Given as list of tuple of ineteger,
                                        where each each tuple is of the following form (y, x)

    :param score_func:      {function}  Score function 

    :param heuristics_func: {function}  Heuristics funtion

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
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int],
                 heuristics_func: abc.Callable[[list[list[bool]], tuple[int, int]], dict[tuple[int, int], int]],
                 printing: bool,
                 **kwargs) -> None:
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
        """
            Find solution function, used as a template for the the main solvers
        
        :param base_constraints:    {list}  Constraints to be condisdered during the solve procedure

        :return:                    {list}  Returns the paths traversed by all agents
        
        """
        raise NotImplementedError
