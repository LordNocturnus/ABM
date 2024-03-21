"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
import typing

from single_agent_planner_v2 import get_location


class DistributedAgent(object):
    """DistributedAgent object to be used in the distributed planner."""

    def __init__(self, my_map: typing.Any, start: tuple[int, int], goal: tuple[int, int], heuristics: typing.Any, agent_id: int
                 ) -> None:
        """
        my_map   - list of lists specifying obstacle positions
        starts      - (x1, y1) start location
        goals       - (x1, y1) goal location
        heuristics  - heuristic to goal location
        """
        # raise NotImplementedError
        self.my_map = my_map
        self.start = start
        self.goal = goal
        self.id = agent_id
        self.heuristics = heuristics
        self.path = None

        self.view_radius = 2
        self.forward_transfer = 2

        self.intent = None
        self.memory = {}

    def update_path(self, path):
        self.path = path

    def get_intent(self, timestep):

        #### !!!!!!!!! CAUSES BUGS / ISSUES

        # self.intent = self.path[timestep:timestep + self.forward_transfer + 1]
        # self.intent = [get_location(self.path, timestep + dt) for dt in range(self.forward_transfer + 1)]
        # return self.path[timestep:timestep + self.forward_transfer + 1]

        self.intent = [get_location(self.path, timestep + dt) for dt in range(self.forward_transfer + 1)]
        return self.intent

    def update_memory(self, path, agent):
        self.memory[agent] = path

    def clear_memory(self):
        self.memory = {}

    def solve_conflict(self, timestep):

        own_path    = self.intent
        others_path = self.memory

        # Solve the conflict if exists, only knowing the agents full path and the intent of the others

        raise NotImplementedError

    def get_vision(self):
        raise NotImplementedError
        return vision