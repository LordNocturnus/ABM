"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
import typing

from single_agent_planner import get_location, a_star


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

        self.view_radius = 10
        self.forward_transfer = 10

        self.intent = None
        self.memory = {}

        self.constraint_table_local = []
        self.constraint_table_transfer = []

    def update_path(self, path):
        self.path = path

    def get_intent(self, timestep):

        #### !!!!!!!!! CAUSES BUGS / ISSUES

        # self.intent = self.path[timestep:timestep + self.forward_transfer + 1]
        # if self.intent == []:
        #     self.intent = [self.goal]*2

        if self.intent == []:
            self.intent = [self.goal] * 2
        else:
            self.intent = [get_location(self.path, timestep + dt) for dt in range(self.forward_transfer + 1)]

        return self.intent

    def update_memory(self, path, agent, remaining):
        self.memory[agent] = {'path': path, 'cost': remaining}

    def clear_memory(self):
        self.memory = {}

    def solve_conflict(self, timestep):

        # Solve the conflict if exists, only knowing the agents full path and the intent of the others
        # Idea 1 give priority to the first agent (Thus the agent seing the other ones)

        if not self.memory:
            # No collision
            return []

        if not self.check_collisions():
            # No collision
            return []

        # Solve collision
        for observed_agent_id, observed_agent_data in self.memory.items():

            if observed_agent_data['cost'] > len(self.path):

                vertexes = observed_agent_data['path']
                edges = [[vertexes[i], vertexes[i + 1]] for i in range(len(vertexes) - 1)]

                for id_vertex, vertex in enumerate(vertexes):
                    self.constraint_table_local.append(
                        {'positive': False, 'agent': self.id, 'loc': [vertex],
                         'timestep': timestep + id_vertex})

                for id_edge, edge in enumerate(edges):
                    self.constraint_table_local.append(
                        {'positive': False, 'agent': self.id, 'loc': edge[::-1],
                         'timestep': timestep + id_edge + 1})

            else:

                vertexes = self.intent
                edges = [[vertexes[i], vertexes[i + 1]] for i in range(len(vertexes) - 1)]

                for id_vertex, vertex in enumerate(vertexes):
                    self.constraint_table_transfer.append(
                        {'positive': False, 'agent': observed_agent_id, 'loc': [vertex],
                         'timestep': timestep + id_vertex})

                for id_edge, edge in enumerate(edges):
                    self.constraint_table_transfer.append(
                        {'positive': False, 'agent': observed_agent_id, 'loc': edge[::-1],
                         'timestep': timestep + id_edge + 1})

        self.plan_path(timestep)

        return self.constraint_table_transfer

    def get_vision(self):
        raise NotImplementedError
        return vision

    def plan_path(self, timestep):
        path = a_star(self.my_map, self.start, self.goal, self.heuristics,
                      self.id, self.constraint_table_local)
        if path is None:
            raise BaseException('No solutions')
        self.update_path(path)

    def add_constraint(self, constraint):
        self.constraint_table_local.append(constraint)

    def check_collisions(self):

        path1 = self.intent

        for path2 in [el['path'] for el in self.memory.values()]:
            for i in range(max(len(path1), len(path2))):
                # Vertex collision
                if get_location(path1, i) == get_location(path2, i):

                    return True

                # Edge collision
                elif [get_location(path1, i), get_location(path1, i + 1)] == [get_location(path2, i + 1),
                                                                              get_location(path2, i)]:
                    return True

        return False