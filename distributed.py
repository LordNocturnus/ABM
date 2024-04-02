"""
This file contains a placeholder for the DistributedPlanningSolver class that can be used to implement distributed planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""

import time as timer

import collisions
import copy
from single_agent_planner_v2 import compute_heuristics, get_sum_of_cost, get_location
from distributed_agent_class import DistributedAgent
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
        self.heuristics: list[dict[tuple[int, int], int]] = []

        # compute heuristics for the low-level search
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

        self.agents: list[DistributedAgent] = []
        # T.B.D.
        
    def find_solution(self, cbs=False) -> list[list[tuple[int, int]]]:
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
            self.agents.append(DistributedAgent(self.my_map, self.starts[i], self.goals[i],
                                                compute_heuristics(self.my_map, self.goals[i]), i))

        # Main planning loop

        # while loop for goals reached
        # for each agent create field of view (fov)
        # if agent is in view communicate current location and x amount of locations of the path
        # if collision on x amount of locations of path, communicate length of remainder path
        # create new path
        # path of agent.id and path of agent(id of state)
        # constrainst for agent with shorter len(path)

        timestep = 0

        while not all([a.finished for a in self.agents]):

            print(f"===T=== |>{timestep}<| ===T===")
            found_collision = True
            col = 0
            while found_collision:
                print(f"===C=== |>{col}<| ===C===")
                found_collision = False
                messages = {}
                for agent in self.agents:
                    print(f"===A=== |>{agent.id}<| ===A===")
                    fov = agent.get_view(self.my_map)  # field_of_view
                    visible_agents = [a for a in self.agents if a.pos in fov and not a == agent]
                    if len(visible_agents) == 0:
                        continue
                    colliding_agents = [a for a in visible_agents if collisions.detect_collision(0,
                                                                                                 0,
                                                                                                 a.get_path(),
                                                                                                 agent.get_path())]
                    if len(colliding_agents) == 0:
                        continue
                    found_collision = True
                    messages[agent.id] = set([copy.deepcopy(a.message) for a in colliding_agents])

                for idx in messages.keys():
                    try:
                        self.agents[idx].run_prio(messages[idx])
                    except ValueError:
                        pass
                    #print(self.agents[idx].path[:-1] + self.agents[idx].planned_path)
                    """for other_agent in visible_agents:
                        reaction = other_agent.get_reaction(agent.get_path_message())
                        if reaction is not None:
                            found_collision = True
                            own_reaction = agent.get_reaction(other_agent.get_path_message())
                            print(reaction, own_reaction)
                    #if len(reactions) == 0:
                    #    continue
                    print("debug")"""
                col += 1
                #break

            # move every agent by one step
            for agent in self.agents:
                agent.step(self.my_map)
                #print(agent.id, agent.pos)
            #break

            timestep += 1

        # Get final result
        for i in range(self.num_of_agents):  # Find path for each agent
            result[i] = self.agents[i].path + self.agents[i].planned_path

        # Print final output
        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))  # Hint: think about how cost is defined in your implementation
        print(result)
        
        return result  # Hint: this should be the final result of the distributed planning (visualization is done after planning)

    """def goals_reached(self, paths: list[list[tuple[int, int]]], timestep: int) -> bool:
        # goals = self.goals
        # location agents = get_location(path, timestep)
        # number/index agent = self.num_of_agents() -> loop over
        # have all goals been reached

        for i in range(self.num_of_agents):
            if get_location(paths[i], timestep) != self.goals[i]:
                return False

        return True

    def check_collisions(self, paths: list[list[tuple[int, int]]]) -> bool:

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

        return result  # """