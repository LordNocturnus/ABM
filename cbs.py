import time as timer
import heapq
import random
import typing
from copy import deepcopy

from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost


def detect_collision(agent1: int, agent2: int, path1: list[tuple[int, int]], path2: list[tuple[int, int]]) -> None:
    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.

    for i in range(max(len(path1), len(path2))):
        # Vertex collision
        if get_location(path1, i) == get_location(path2, i):
            return {'a1': agent1, 'a2': agent2, 'loc': [get_location(path1, i)], 'timestep': i}
        
        # Edge collision
        elif [get_location(path1, i), get_location(path1, i+1)] == [get_location(path2, i + 1), get_location(path2, i)]:
            return {'a1': agent1, 'a2': agent2, 'loc': [get_location(path1, i), get_location(path1, i+1)], 'timestep': i + 1}

    return None


def detect_collisions(paths: list[list[tuple[int, int]]]) -> None:
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.

    collisions = []

    for agent_1 in range(len(paths)):
        for agent_2 in range(agent_1 + 1, len(paths)):
            collisions.append(detect_collision(agent_1, agent_2, paths[agent_1], paths[agent_2]))

    return [el for el in collisions if el is not None]
    # return collisions


def standard_splitting(collision: typing.Any) -> None:
    ##############################
    # Task 3.2: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the second agent to be at the
    #                            specified location at the specified timestep.
    #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the second agent to traverse the
    #                          specified edge at the specified timestep
    out = [{'positive': False, 'agent': collision['a1'], 'loc': collision['loc'], 'timestep': collision['timestep']},
           {'positive': False, 'agent': collision['a2'], 'loc': collision['loc'][::-1], 'timestep': collision['timestep']}]
    return out


def disjoint_splitting(collision: typing.Any) -> None:
    ##############################
    # Task 4.1: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the same agent to be at the
    #                            same location at the timestep.
    #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the same agent to traverse the
    #                          specified edge at the specified timestep
    #           Choose the agent randomly

    val = random.random()

    if 0 <= val <= 0.5:
        rng_agent = collision['a1']
    elif 0.5 <= val <= 1:
        rng_agent = collision['a2']

    out = [{'positive': True, 'agent': rng_agent, 'loc': collision['loc'], 'timestep': collision['timestep']},
           {'positive': False, 'agent': rng_agent, 'loc': collision['loc'], 'timestep': collision['timestep']}]

    return out


class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map: list[list[bool]], starts: list[tuple[int, int]], goals: list[tuple[int, int]]) -> None:
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time: float = 0.0
        self.start_time: float = 0.0

        self.open_list: list[typing.Any] = []

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node: typing.Any) -> None:
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        # print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self) -> typing.Any:
        _, _, id, node = heapq.heappop(self.open_list)
        # print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint: bool=True) -> list[list[tuple[int, int]]]:
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()

        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        root = {'cost': 0,
                'constraints': [],
                'paths': [],
                'collisions': []}
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root['constraints'])
            if path is None:
                raise BaseException('No solutions')
            root['paths'].append(path)

        root['cost'] = get_sum_of_cost(root['paths'])
        root['collisions'] = detect_collisions(root['paths'])
        self.push_node(root)

        # Task 3.1: Testing
        print(root['collisions'])

        # Task 3.2: Testing
        for collision in root['collisions']:
            print(standard_splitting(collision))

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit

        while self.open_list:

            P = self.pop_node()

            if not P['collisions']:
                print(f"Constraint utelised {P['constraints']}")
                print(f"Paths utelised {P['paths']}")
                return P['paths']

            one_collision = standard_splitting(P['collisions'][0])
            one_collision = disjoint_splitting(P['collisions'][0])

            # Solve collision
            for collision_constraint in one_collision:

                Q = {'constraints': deepcopy(P['constraints']) + [collision_constraint],
                     'paths': deepcopy(P['paths'])}

                i = collision_constraint['agent']

                path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                              i, Q['constraints'])

                if path:
                    Q['paths'][i] = path
                    Q['collisions'] = detect_collisions(Q['paths'])
                    Q['cost'] = get_sum_of_cost(Q['paths'])
                    self.push_node(Q)

        # self.print_results(root)
        # return root['paths']
            print(len(self.open_list))
            
        # Return nothing if no solution is found
        return []

    def print_results(self, node: typing.Any) -> None:
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(node['paths'])))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
