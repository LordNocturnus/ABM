from copy import deepcopy
import time as timer
import heapq
import typing
import constraints
import collisions

from single_agent_planner_v2 import compute_heuristics, a_star, get_sum_of_cost


class CBSNode:

    def __init__(self,
                 cost: int,
                 constraint_list: list[constraints.Constraint],
                 paths: list[list[tuple[int, int]]],
                 collision_dict: dict[tuple[int, int], collisions.Collision],
                 idx: int) -> None:
        self.cost = cost
        self.constraints = constraint_list
        self.paths = paths
        self.collisions = collision_dict
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
        node: CBSNode = heapq.heappop(self.open_list)
        #print("Expand node {}".format(node.idx))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint: bool = True,
                      constraint_list: list[constraints.Constraint] = None) -> list[list[tuple[int, int]]]:
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()

        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        print(constraint_list)
        if constraint_list:
            root = CBSNode(0, constraint_list, [], dict(), 0)
        else:
            root = CBSNode(0, [], [], dict(), 0)
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root.constraints)
            if path is None:
                raise BaseException('No solutions')
            root.paths.append(path)

        root.cost = get_sum_of_cost(root.paths)
        root.collisions = collisions.detect_collisions(root.paths)
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
                #self.print_results(root)
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
                    new.collisions = collisions.detect_collisions(new.paths)
                    new.cost = get_sum_of_cost(new.paths)
                    self.push_node(new)
            #print(len(self.open_list))

        raise BaseException('No solutions')#"""

    def print_results(self, node: CBSNode) -> None:
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(node.paths)))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
