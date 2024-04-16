from collections import abc
import time as timer
import heapq
import typing
import constraints
import collisions

from single_agent_planner_v2 import compute_heuristics, a_star, get_sum_of_cost
import base_solver


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


class CBSSolver(base_solver.BaseSolver):
    """The high-level search of CBS."""

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
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """
        super().__init__(my_map, starts, goals, score_func, heuristics_func, printing)
        self.disjoint = disjoint

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.start_time: float = 0.0

        self.open_list: list[typing.Any] = []

    def push_node(self, node: CBSNode) -> None:
        heapq.heappush(self.open_list, node)
        self.num_of_generated += 1

    def pop_node(self) -> CBSNode:
        node: CBSNode = heapq.heappop(self.open_list)
        self.num_of_expanded += 1
        return node

    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()

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
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(self.score_func(node.paths)))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
