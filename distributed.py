"""
This file contains a placeholder for the DistributedPlanningSolver class that can be used to implement distributed planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""

import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost, get_location
from distributed_agent_class import DistributedAgent
from cbs import detect_collision, detect_collisions
import view

class DistributedPlanningSolver(object):
    """A distributed planner"""

    def __init__(self,
                 my_map: list[list[bool]],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]]) -> None:
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """
        self.CPU_time: float = 0.0
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.heuristics: list[list[int]] = []

        # compute heuristics for the low-level search
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

        self.agents: list[object] = []
        # T.B.D.
        
    def find_solution(self) -> list[list[tuple[int, int]]]:
        """
        Finds paths for all agents from start to goal locations. 
        
        Returns:
            result (list): with a path [(s,t), .....] for each agent.
        """
        # Initialize constants       
        start_time = timer.time()
        result: list[list[tuple[int, int]]] = [[]] * self.num_of_agents
        self.CPU_time = timer.time() - start_time
        
        # Initialization of agents
        # Create agent objects with DistributedAgent class
        for i in range(self.num_of_agents):
            self.agents.append(DistributedAgent(self.my_map, self.starts[i], self.goals[i], self.heuristics[i], i))

        ## Path finding procedure

        constraints_list = []
        # First base planning
        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, [])
            if path is None:
                raise BaseException('No solutions')
            self.agents[i].update_path(path)
            result[i] = path

        # Main planning loop

        # while loop for goals reached
        # for every timestep for every agent find position of agent
        # for each agent create view
        # if agent is in view communicate current location and x amount of locations of the path
        # if collision on x amount of locations of path, communicate length of remainder path
        # create new path
        # path of agent.id and path of agent(id of state)
        # constrainst for agent with shorter len(path)

        timestep = 0

        while not self.goals_reached(result, timestep) or self.check_collisions(result):

            print(f"======= |>{timestep}<| =======")
            for agent in self.agents:

                location_agents = [get_location(result[el.id], timestep) for el in self.agents]
                agents_in_view = view.fov(agent.id, location_agents, agent.view_radius)

                # communicate path
                vertexes = agent.get_intent(timestep)
                edges = [[vertexes[i], vertexes[i + 1]] for i in range(len(vertexes) - 1)]

                # Create priority order, to evaluate the agents
                # |> [False, True, False, False, True] (View of agent 0)

                # Update the agent there knowledge of the suroundings
                for observed_agent in self.agents:

                    if not agents_in_view[observed_agent.id]:
                        continue

                    # Get the intent of the other agent
                    vertexes_a2 = observed_agent.get_intent(timestep)
                    edges_a2    = [[vertexes_a2[i], vertexes_a2[i + 1]] for i in range(len(vertexes_a2) - 1)]

                    agent.update_memory(vertexes_a2, observed_agent.id, len(observed_agent.path))

                # Solve the collisions for that agent using the aquired knowledge

                to_others = agent.solve_conflict(timestep)

                for c in to_others:
                    self.agents[c['agent']].add_constraint(c)

                agent.clear_memory()

            result = [self.agents[i].path for i in range(self.num_of_agents)]

            timestep += 1


        # Print final output
        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))  # Hint: think about how cost is defined in your implementation
        print(result)
        
        return result  # Hint: this should be the final result of the distributed planning (visualization is done after planning)

    def goals_reached(self, paths, timestep) -> bool:
        # goals = self.goals
        # location agents = get_location(path, timestep)
        # number/index agent = self.num_of_agents() -> loop over
        # have all goals been reached

        for i in range(self.num_of_agents):
            if get_location(paths[i], timestep) != self.goals[i]:
                return False

        return True

    def check_collisions(self, paths):

        for agent_1 in range(len(paths)):
            for agent_2 in range(agent_1 + 1, len(paths)):

                path1 = paths[agent_1]
                path2 = paths[agent_2]

                for i in range(max(len(path1), len(path2))):
                    # Vertex collision
                    if get_location(path1, i) == get_location(path2, i):

                        return True

                    # Edge collision
                    elif [get_location(path1, i), get_location(path1, i + 1)] == [get_location(path2, i + 1),
                                                                                  get_location(path2, i)]:
                        return True

        return False

    def base_planning(self, constraints):
        result: list[list[tuple[int, int]]] = [[]] * self.num_of_agents

        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints)
            if path is None:
                raise BaseException('No solutions')
            self.agents[i].update_path(path)
            result[i] = path

        return result