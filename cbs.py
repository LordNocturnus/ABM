from collections import abc
import time as timer
import heapq
import typing
import constraints
import collisions

from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost
import base_solver


class CBSNode:
    """
        Individual node on the tree generated by CBS. Primarily used as a memory object to simplify code
        understandability

    :param cost:        {int}   Cost of the paths planned in this Node base on the chosen cost function
    :param constraints: {list}  Constraints used for planning the paths
    :param paths:       {list}  Currently planned paths
    :param collisions:  {dict}  All occurring collisions in the paths indexed by a tuple of indices of the colliding
                                agents
    :param idx:         {int}   Unique index of the node
    """

    def __init__(self,
                 cost: int,
                 constraint_list: list[constraints.Constraint],
                 paths: list[list[tuple[int, int]]],
                 collision_dict: dict[tuple[int, int], collisions.Collision],
                 idx: int) -> None:
        """
            Initialization function of the CBSNode

        :param cost:            {int}   Cost of the paths planned in this Node base on the chosen cost function
        :param constraint_list: {list}  Constraints used for planning the paths
        :param paths:           {list}  Currently planned paths
        :param collision_dict:  {dict}  All occurring collisions in the paths indexed by a tuple of indices of the colliding
                                        agents
        :param idx:             {int}   Unique index of the node
        """
        self.cost = cost
        self.constraints = constraint_list
        self.paths = paths
        self.collisions = collision_dict
        self.idx = idx

    def __lt__(self, other: "CBSNode") -> bool:
        """
            Less than comparison between two CBSNodes where first the cost is considered then the number of remaining
            collisions and lastly the indices

        :param other:   {CBSNode}   Node to compare self with

        :return:        {bool}      index of self is less than index of other
        :return:        {bool}      number of collisions in self is less than number of collisions in other
        :return:        {bool}      cost of self is less than cost of other

        :raise:                     ValueError
        """
        if self.cost == other.cost:
            if len(self.collisions) == len(other.collisions):
                if self.idx == other.idx:
                    raise ValueError("something does not work properly")
                return self.idx < other.idx
            return len(self.collisions) < len(other.collisions)
        return self.cost < other.cost


class CBSSolver(base_solver.BaseSolver):
    """
        Conflict Based Search (CBS) Solver for multi agent global pathfinding.

    :param CPU_time:            {float}     Value to keep track of the cpu time required for the solver to complete the
                                        planning
    :param my_map:              {list}      List of list of boolean, describing the map environment. True indicates a
                                            wall.
    :param starts:              {list}      List of starting positions for the agents. Given as list of tuple of
                                            integer, where each each tuple is of the following form (y, x)
    :param goals:               {list}      List of goal/ end positions for the agents. Given as list of tuple of
                                            integer, where each each tuple is of the following form (y, x)
    :param score_func:          {function}  Score function
    :param heuristics_func:     {function}  Heuristics function
    :param printing:            {bool}      Variable to enable and disable printing within the model. This allows for
                                            the user to specify if they would like to receive the solver outcome after
                                            every run or not. True enables printing while false disables this behaviour.
    :param num_of_agents:       {int}       The number of agents within the environment. Extracted from the supplied
                                            goal or start positions.
    :param heuristics:          {list}      List containing the heuristics.
    :param disjoint:            {bool}      Flag controlling if disjoint splitting should be used
    :param num_of_expanded:     {bool}      Counter for nodes that where explored by the search
    :param num_of_generated:    {bool}      Counter for nodes that where created by the search
    :param open_list:           {bool}      Heap used to contain and sort nodes during path planning
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
                 disjoint: bool = True,
                 **kwargs) -> None:
        """
            Initialise an instance of the CBSSolver class.

        :param my_map:          {list}      List of list of boolean, describing the map environment. True indicates a
                                            wall.
        :param starts:          {list}      List of starting positions for the agents. Given as list of tuple of
                                            integer, where each each tuple is of the following form (y, x).
        :param goals:           {list}      List of goal/end positions for the agents. Given as list of tuple of
                                            integer, where each each tuple is of the following form (y, x).
        :param score_func:      {function}  Score function
        :param heuristics_func: {function}  Heuristics function
        :param printing:        {bool}      Flag to enable and disable printing within the model. This allows for the
                                            user to specify if they would like to receive the solver outcome after every
                                            run or not. True enables printing while false disables this behaviour.
        :param disjoint:        {bool}      Flag controlling if disjoint splitting should be used
        """
        super().__init__(my_map, starts, goals, score_func, heuristics_func, printing)
        self.disjoint = disjoint

        self.num_of_generated = 0
        self.num_of_expanded = 0

        self.open_list: list[typing.Any] = []

    def push_node(self, node: CBSNode) -> None:
        """
            Push given node onto the open_list heap and increment the counter for generated nodes

        :param node:    {CBSNode}   Node to push onto the heap
        """
        heapq.heappush(self.open_list, node)
        self.num_of_generated += 1

    def pop_node(self) -> CBSNode:
        """
            Pop node from the open_list heap and increment the counter for expanded nodes

        :return:    {CBSNode}   Next node to use in path planning
        """
        node: CBSNode = heapq.heappop(self.open_list)
        self.num_of_expanded += 1
        return node

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """
            runs the CBS algorithm by first initializing a root-node with the provided base_constraints and calculating
            paths base on those. For every node on the heap then first checks if there are no more collisions and
            returns the agent paths if true. Otherwise expands the first collision into new constraints and creates a
            new node for each of the two constraints to then be put onto the heap.

        :param base_constraints:    {list}  List of external constraints to restrict path planning

        :return:                    {List}  Paths traversed by all agents

        :raise:                             BaseException
        :raise:                             BaseException
        """

        start_time = timer.time()

        root = CBSNode(0, [*base_constraints], [], dict(), 0)
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root.constraints)
            if path is None:
                raise BaseException('No solutions')
            root.paths.append(path)

        root.cost = self.score_func(root.paths)
        root.collisions = collisions.detect_collisions(root.paths)
        self.push_node(root)

        while len(self.open_list) > 0:
            current = self.pop_node()
            if len(current.collisions) == 0:
                self.CPU_time = timer.time() - start_time
                if self.printing:
                    self.print_results(current)
                return current.paths
            if self.disjoint:
                new_constraints = current.collisions[next(iter(current.collisions))].disjoint_splitting()
            else:
                new_constraints = current.collisions[next(iter(current.collisions))].standard_splitting()

            for constraint in new_constraints:
                new = CBSNode(0,
                              current.constraints + [constraint],
                              [*current.paths], dict(), self.num_of_generated)
                path = a_star(self.my_map,
                              self.starts[constraint.agent],
                              self.goals[constraint.agent],
                              self.heuristics[constraint.agent],
                              constraint.agent, new.constraints)
                if path:
                    new.paths[constraint.agent] = path
                    new.collisions = collisions.detect_collisions(new.paths)
                    new.cost = self.score_func(new.paths)
                    self.push_node(new)

        raise BaseException('No solutions')

    def print_results(self, node: CBSNode) -> None:
        """
            print results of CBS

        :param node:    {CBSNode}   node to use as reference for path printing
        """
        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(self.score_func(node.paths)))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
