import numpy as np
import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost, get_location

import warnings


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = []
        constraints = []

        # constraints.append({'positive': False, 'agent': 1, 'loc': [(2, 4)], 'timestep': 3})
        # constraints.append({'positive': False, 'agent': 1, 'loc': [(2, 3)], 'timestep': 2})
        # constraints.append({'positive': False, 'agent': 1, 'loc': [(2, 2)], 'timestep': 1})

        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)

            for id, path_vertex in enumerate(path):
                if id == len(path) - 1:
                    for dt in range(20):
                        constraints.append(
                            {'positive': True, 'agent': i, 'loc': [path[-1]], 'timestep': id + dt})
                constraints.append({'positive': True, 'agent': i, 'loc': [path_vertex, path[min(id+1, len(path)-1)]], 'timestep': id + 1})


                """for agent in range(i+1, self.num_of_agents):

                    #constraints.append({'positive': False, 'agent': agent, 'loc': [path_vertex], 'timestep': id})

                    if id != len(path) - 1:
                        pass
                        #travel = [path[id+1], path[id]]
                        #constraints.append({'positive': False, 'agent': agent, 'loc': travel, 'timestep': id+1})
                    else:
                        for dt in range(20):
                            constraints.append(
                                {'positive': False, 'agent': agent, 'loc': [path[-1]], 'timestep': id + dt})#"""

            for p in result[:-1]:
                for i in range(max(len(path), len(p))):
                    if np.linalg.norm(np.asarray(get_location(p, i)) - np.asarray(get_location(path, i))) < 0.7:
                        with warnings.catch_warnings():
                            warnings.simplefilter("always")
                            warnings.warn("COLLISION!!!")


            ##############################
            # Task 2: Add constraints here
            #         Useful variables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraints: array of constraints to consider for future A* searches


            ##############################

        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        print(result)
        return result
