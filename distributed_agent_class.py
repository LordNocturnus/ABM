"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
import copy
import typing

import collisions
import constraints
from single_agent_planner_v2 import get_location, a_star
from cbs import CBSSolver
from prioritized import PrioritizedPlanningSolver


class DistributedAgent(object):
    """DistributedAgent object to be used in the distributed planner."""

    def __init__(self,
                 my_map: list[list[bool]],
                 start: tuple[int, int],
                 goal: tuple[int, int],
                 heuristics: dict[tuple[int, int], int],
                 agent_id: int
                 ) -> None:
        """
        my_map   - list of lists specifying obstacle positions
        starts      - (x1, y1) start location
        goals       - (x1, y1) goal location
        heuristics  - heuristic to goal location
        """
        self.my_map = my_map
        #self.start = start
        self.pos = start
        self.goal = goal
        self.id = agent_id
        self.heuristics = heuristics

        ## Path finding procedure
        planned_path = a_star(my_map, self.pos, self.goal, self.heuristics, self.id, [])
        if planned_path is None:
            raise ValueError('No solutions')
        else:
            self.planned_path = planned_path

        #self.view_radius = 5
        #self.forward_transfer = 5
        self.path = [self.pos]

        self.intent = None
        self.memory: set[tuple[tuple[int, int], tuple[int, int], int, int]] = {self.message}

    @property
    def finished(self) -> bool:
        return self.pos == self.goal

    def step(self, my_map: list[list[bool]]) -> None:
        self.path.append(self.pos)
        self.pos = self.planned_path[min(1, len(self.planned_path) - 1)]  # update pos to position of next timestep

        # Update all constraints to apply one step earlier
        self.memory = {self.message}

        self.planned_path = self.planned_path[min(1, len(self.planned_path) - 1):]

    def get_view(self, my_map: list[list[bool]]) -> list[tuple[int, int]]:
        """
        returns every coordinate visible to this agent
        """
        ret = []
        for x in range(len(my_map)):
            for y in range(len(my_map[x])):
                if not my_map[x][y]:
                    ret.append((x, y))
        return ret

    def get_path(self, lim: typing.Optional[int] = None) -> list[tuple[int, int]]:
        if lim:
            return self.planned_path[0:min(lim, len(self.planned_path) - 1)]
        else:
            return self.planned_path

    @property
    def message(self) -> tuple[tuple[int, int], tuple[int, int], int, int]:
        return self.pos, self.goal, len(self.planned_path), self.id

    def run_cbs(self, other_pos: list[tuple[int, int]], other_goal: list[tuple[int, int]], disjoint: bool = False) -> None:
        solver = CBSSolver(self.my_map, [self.pos] + other_pos, [self.goal] + other_goal)
        res = solver.find_solution(disjoint)
        self.planned_path = res[0]

    def run_prio(self, messages: set[tuple[tuple[int, int], tuple[int, int], int, int]]) -> None:
        self.memory = self.memory.union(messages)
        restrictions = sorted(self.memory, key=lambda x: x[2], reverse=True)
        #print(restrictions)
        solver = PrioritizedPlanningSolver(self.my_map, [a[0] for a in restrictions], [a[1] for a in restrictions])
        res = solver.find_solution(recursive=False)
        for i, path in enumerate(res):
            if restrictions[i][3] == self.id:
                self.planned_path = path
