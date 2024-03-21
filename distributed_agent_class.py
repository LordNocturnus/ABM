"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
import typing

from single_agent_planner_v2 import get_location


class DistributedAgent(object):
    """DistributedAgent object to be used in the distributed planner."""

    def __init__(self, my_map: typing.Any, start: tuple[int, int], goal: tuple[int, int], heuristics: typing.Any, agent_id: int,
                 view_radius: int) -> None:
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

        self.memory = {}

    def update_path(self, path):
        self.path = path

    def get_intent(self, timestep):
        return self.path[timestep:timestep + self.forward_transfer + 1]