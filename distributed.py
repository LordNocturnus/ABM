"""
This file contains a placeholder for the DistributedPlanningSolver class that can be used to implement distributed planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
import multiprocessing
import time as timer

import collisions
import copy
import itertools


import distributed_agent
from single_agent_planner_v2 import compute_heuristics, get_sum_of_cost, get_location
from distributed_agent import DistributedAgent
from prioritized import PrioritizedPlanningSolver
from cbs import CBSSolver
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

        self.visibility_map = dict()
        self.collision_map = dict()
        self.prev_collisions = dict()
        self.global_constraints = []

        self.agents: list[DistributedAgent] = []
        # T.B.D.
        
    def find_solution(self, cbs: bool = False) -> list[list[tuple[int, int]]]:
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
            self.calculate_visibility()
            col = 0
            while self.collision_avoidance():
                print(f"===C=== |>{col}<| ===C===")
                col += 1
                #break

            # move every agent by one step
            for agent in self.agents:
                agent.step()
                #print(agent.id, agent.pos)
            #break

            timestep += 1

        # Get final result
        for i in range(self.num_of_agents):  # Find path for each agent
            result[i] = self.agents[i].path + self.agents[i].planned_path

        self.CPU_time = timer.time() - start_time

        # Print final output
        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))  # Hint: think about how cost is defined in your implementation
        print(result)
        
        return result

    def calculate_visibility(self) -> None:

        for agent in self.agents:
            fov = agent.get_view()  # field_of_view
            visible = [a.id for a in self.agents if a.pos in fov and not a == agent]

            if len(visible) != 0:
                self.visibility_map[agent.id] = visible

    def calculate_collisions(self) -> None:
        self.collision_map = dict()
        for idx in self.visibility_map.keys():
            collision_list = []
            for idx_2 in self.visibility_map[idx]:
                collision = collisions.detect_collision(idx, idx_2,
                                                        self.agents[idx].get_path(), self.agents[idx_2].get_path())
                if collision:
                    collision_list.append(collision)
            if len(collision_list) != 0:
                self.collision_map[idx] = collision_list

    def check_repeating_collisions(self) -> collisions.Collision:
        for key in self.collision_map.keys():
            if key in self.prev_collisions.keys():
                for c in self.collision_map[key]:
                    for c2 in self.prev_collisions[key]:
                        if c == c2:
                            return c
        self.prev_collisions = self.collision_map

    def collision_avoidance(self) -> bool:
        self.calculate_collisions()
        if len(self.collision_map) == 0:
            return False

        repeat = self.check_repeating_collisions()
        if repeat:
            constraint_0, constraint_1 = repeat.standard_splitting()
            if len(self.agents[repeat.agent_0].planned_path) < len(self.agents[repeat.agent_1].planned_path):
                self.global_constraints.append(constraint_0)
            else:
                self.global_constraints.append(constraint_1)
            #raise ValueError("Found Repeating Collision")

        messages = []
        agents_to_run = []
        for idx in self.collision_map.keys():
            messages.append(set([self.agents[c.agent_1].message for c in self.collision_map[idx]]))
            agents_to_run.append(self.agents[idx])

        #print(len(messages), len(self.global_constraints))

        for idx in range(len(messages)):
            self.agents[agents_to_run[idx].id] = distributed_agent.run_cbs(agents_to_run[idx], messages[idx], self.global_constraints)

        """with multiprocessing.Pool(processes=len(agents_to_run)) as pool:
            res = pool.starmap(distributed_agent_class.run_cbs,
                               zip(agents_to_run, messages, itertools.repeat(self.global_constraints)))
        for a in res:
            self.agents[a.id] = a"""
        return True


