"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
import typing

import collisions
import constraints
from single_agent_planner_v2 import get_location, a_star


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
        self.memory: dict[int, list[constraints.Constraint]] = {}

    @property
    def finished(self) -> bool:
        return self.pos == self.goal

    def get_constraints(self, id: typing.Optional[int] = None) -> list[constraints.Constraint]:
        """
        get all constraints currently in memory except for agent with provided id
        """
        ret = []
        for key in self.memory.keys():
            if not key == id:
                ret.extend(self.memory[key])
        return ret

    def step(self, my_map: list[list[bool]]) -> None:
        self.path.append(self.pos)
        self.pos = self.planned_path[min(1, len(self.planned_path) - 1)]  # update pos to position of next timestep

        # Update all constraints to apply one step earlier
        self.memory = {}
        """for key in self.memory.keys():
            for constraint in self.memory[key]:
                constraint.step -= 1 # TODO: consider dropping constraints that nolonger apply aka have step"""

        planned_path = a_star(my_map, self.pos, self.goal, self.heuristics, self.id, [])
        if planned_path is None:
            raise ValueError('No solutions')
        else:
            self.planned_path = planned_path

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

    def get_path_message(self, lim: typing.Optional[int]=None) -> list[tuple[int, int]]:
        if lim:
            return self.planned_path[0:min(lim, len(self.planned_path) - 1)]
        else:
            return self.planned_path

    def get_reaction(self, other_path: list[tuple[int, int]], other_id: int, my_map: list[list[bool]]) -> typing.Optional[tuple[collisions.Collision, int, int]]:
        """
        returns none if no collision found
        otherwise returns tuple containing:
            - Collision instance
            - cost of current path
            - cost of path avoiding collision (-1 if avoiding is impossible)
        """
        collision = collisions.detect_collision(self.id, other_id, self.path, other_path)
        if collision is None:
            return None
        else:
            current = len(self.planned_path)
            constraint_0, constraint_1 = collision.standard_splitting()
            if constraint_0.agent == self.id:
                new_path = a_star(my_map, self.pos, self.goal, self.heuristics, self.id,
                                  self.get_constraints(other_id) + [constraint_0])
                if new_path is None:
                    new = -1
                else:
                    new = len(new_path)
            else:
                new_path = a_star(my_map, self.pos, self.goal, self.heuristics, self.id,
                                  self.get_constraints(other_id) + [constraint_1])
                if new_path is None:
                    new = -1
                else:
                    new = len(new_path)
            print(current, new)
            return collision, current, new


