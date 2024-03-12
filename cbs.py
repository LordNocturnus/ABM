from copy import deepcopy
import time as timer
import heapq
import typing
import constraints
import utils

from single_agent_planner_v2 import compute_heuristics, a_star, get_location, get_sum_of_cost


class Collision:

    def __init__(self,
                 agent_0: int,
                 agent_1: int,
                 step: int,
                 loc_0: tuple[int, int],
                 loc_1: typing.Optional[tuple[int, int]] = None) -> None:
        self.agent_0 = agent_0
        self.agent_1 = agent_1
        self.step = step
        self.loc_0 = loc_0
        self.loc_1 = loc_1

    def standard_splitting(self) -> tuple[constraints.Constraint, constraints.Constraint]:
        ##############################
        # Task 3.2: Return a list of (two) constraints to resolve the given collision
        #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
        #                            specified timestep, and the second constraint prevents the second agent to be at the
        #                            specified location at the specified timestep.
        #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
        #                          specified timestep, and the second constraint prevents the second agent to traverse the
        #                          specified edge at the specified timestep
        if self.loc_1:  # Edge collision
            return (constraints.Constraint(False, self.agent_0, self.step, self.loc_0, self.loc_1),
                    constraints.Constraint(False, self.agent_1, self.step, self.loc_1, self.loc_0))
        return (constraints.Constraint(False, self.agent_0, self.step, self.loc_0),
                constraints.Constraint(False, self.agent_1, self.step, self.loc_0))

    def disjoint_splitting(self, rng=utils.RNG) -> tuple[constraints.Constraint, constraints.Constraint]:
        ##############################
        # Task 4.1: Return a list of (two) constraints to resolve the given collision
        #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
        #                            specified timestep, and the second constraint prevents the same agent to be at the
        #                            same location at the timestep.
        #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
        #                          specified timestep, and the second constraint prevents the same agent to traverse the
        #                          specified edge at the specified timestep
        #           Choose the agent randomly
        agent = rng.choice((self.agent_0, self.agent_1))
        if self.loc_1:  # Edge collision
            return (constraints.Constraint(True, agent, self.step, self.loc_0, self.loc_1),
                    constraints.Constraint(False, agent, self.step, self.loc_0, self.loc_1))
        return (constraints.Constraint(True, agent, self.step, self.loc_0),
                constraints.Constraint(False, agent, self.step, self.loc_0))

    def __str__(self):
        if self.loc_1:
            return f"Edge Collision of agent {self.agent_0} and agent {self.agent_1} at timestep {self.step} between {self.loc_0} and {self.loc_1}\n"
        return f"Vertex collision of agent {self.agent_0} and agent {self.agent_1} at timestep {self.step} at location {self.loc_0}\n"

    def __repr__(self):
        return self.__str__()


def detect_collision(agent_0: int,
                     agent_1: int,
                     path_0: list[tuple[int, int]],
                     path_1: list[tuple[int, int]]) -> typing.Optional[Collision]:

    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.
    for i in range(max(len(path_0), len(path_1))):
        if get_location(path_0, i) == get_location(path_1, i):
            return Collision(agent_0, agent_1, i, get_location(path_0, i))
        elif get_location(path_0, i) == get_location(path_1, i + 1) and \
                get_location(path_0, i + 1) == get_location(path_1, i):
            return Collision(agent_0, agent_1, i + 1, get_location(path_0, i), get_location(path_0, i + 1))
    return None


def detect_collisions(paths: list[list[tuple[int, int]]]) -> dict[(int, int), Collision]:
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.
    res: dict[(int, int), Collision] = dict()
    for a0, p0 in enumerate(paths[:-1]):
        for a1, p1 in enumerate(paths[a0 + 1:]):
            collision = detect_collision(a0, a0 + a1 + 1, p0, p1)
            if collision:
                res[(a0, a0 + a1 + 1)] = collision
    return res


"""def standard_splitting(collision: Collision) -> list[constraints.Constraint]:
    ##############################
    # Task 3.2: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the second agent to be at the
    #                            specified location at the specified timestep.
    #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the second agent to traverse the
    #                          specified edge at the specified timestep
    pass"""


def disjoint_splitting(collision: Collision) -> None:
    ##############################
    # Task 4.1: Return a list of (two) constraints to resolve the given collision
    #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
    #                            specified timestep, and the second constraint prevents the same agent to be at the
    #                            same location at the timestep.
    #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
    #                          specified timestep, and the second constraint prevents the same agent to traverse the
    #                          specified edge at the specified timestep
    #           Choose the agent randomly

    raise NotImplementedError


class CBSNode:

    def __init__(self,
                 cost: int,
                 constraint_list: list[constraints.Constraint],
                 paths: list[list[tuple[int, int]]],
                 collisions: dict[(int, int), Collision],
                 idx: int) -> None:
        self.cost = cost
        self.constraints = constraint_list
        self.paths = paths
        self.collisions = collisions
        self.idx = idx

    def __lt__(self, other: "CBSNode") -> bool:
        """Return true is "self" is better than "other"."""
        if self.cost == other.cost:
            if len(self.collisions) == len(other.collisions):
                if self.idx == other.idx:
                    raise ValueError("something does not work properly")
                return self.idx < other.idx
            return len(self.collisions) < len(other.collisions)
        return self.cost < other.cost


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

    def push_node(self, node: CBSNode) -> None:
        heapq.heappush(self.open_list, node)
        #print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self) -> CBSNode:
        node = heapq.heappop(self.open_list)
        #print("Expand node {}".format(node.idx))
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
        root = CBSNode(0, [], [], dict(), 0)
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root.constraints)
            if path is None:
                raise BaseException('No solutions')
            root.paths.append(path)

        root.cost = get_sum_of_cost(root.paths)
        root.collisions = detect_collisions(root.paths)
        self.push_node(root)

        # Task 3.1: Testing
        #print(root.collisions)

        # Task 3.2: Testing
        #for c in root.collisions:
        #    print(root.collisions[c].standard_splitting())

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit

        while len(self.open_list) > 0:
            current = self.pop_node()
            if len(current.collisions) == 0:
                self.print_results(root)
                return current.paths
            #print(current.collisions[next(iter(current.collisions))])
            if disjoint:
                new_constraints = current.collisions[next(iter(current.collisions))].disjoint_splitting()
            else:
                new_constraints = current.collisions[next(iter(current.collisions))].standard_splitting()

            for constraint in new_constraints:
                #print(current.constraints + [constraint])
                new = CBSNode(0,
                              deepcopy(current.constraints) + [constraint],
                              deepcopy(current.paths), dict(), self.num_of_generated)
                path = a_star(self.my_map,
                              self.starts[constraint.agent],
                              self.goals[constraint.agent],
                              self.heuristics[constraint.agent],
                              constraint.agent, new.constraints)
                if path:
                    new.paths[constraint.agent] = path
                    new.collisions = detect_collisions(new.paths)
                    new.cost = get_sum_of_cost(new.paths)
                    self.push_node(new)
            print(len(self.open_list))

        raise BaseException('No solutions')#"""

    def print_results(self, node: CBSNode) -> None:
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(node.paths)))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
