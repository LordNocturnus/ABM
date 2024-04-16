"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""

from collections import abc
import multiprocessing
from multiprocessing import connection

import collisions
import constraints
import single_agent_planner_v2
import base_solver


class DistributedAgent(object):
    """DistributedAgent object to be used in the distributed planner."""

    def __init__(self,
                 my_map: list[list[bool]],
                 start: tuple[int, int],
                 goal: tuple[int, int],
                 view_size: int,
                 path_limit: int,
                 agent_id: int,
                 heuristics_func: abc.Callable[[list[list[bool]], tuple[int, int]], dict[tuple[int, int], int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int],
                 solver: type[base_solver.BaseSolver],
                 **kwargs
                 ) -> None:
        """
        my_map   - list of lists specifying obstacle positions
        starts      - (x1, y1) start location
        goals       - (x1, y1) goal location
        heuristics  - heuristic to goal location
        """
        self.my_map = my_map
        self.pos = start
        self.goal = goal
        self.id = agent_id
        self.heuristics_func = heuristics_func
        self.score_func = score_func
        self.solver = solver
        self.kwargs = kwargs

        if view_size <= 0:
            self.view_size = None
        else:
            self.view_size = view_size

        if path_limit <= 0:
            self.path_limit = None
        else:
            self.path_limit = path_limit

        self.global_constraints = []
        self.path = [self.pos]

        ## Initial Path finding procedure
        planned_path = single_agent_planner_v2.a_star(my_map,
                                                      self.pos,
                                                      self.goal,
                                                      self.heuristics_func(self.my_map, self.goal),
                                                      self.id,
                                                      self.global_constraints)
        if planned_path is None:
            raise ValueError('No solutions')
        else:
            self.planned_path = planned_path

        self.message_memory = [self.message]
        self.collision_memory = []
        self.repeat = None

    @property
    def finished(self) -> bool:
        return self.pos == self.goal

    @property
    def message(self) -> tuple[tuple[int, int], tuple[int, int], int, int]:
        return self.pos, self.goal, len(self.planned_path), self.id

    def get_view(self) -> list[tuple[int, int]]:
        """
            returns every coordinate visible to this agent
        """
        ret = []
        for x in range(len(self.my_map)):
            for y in range(len(self.my_map[x])):
                if not self.my_map[x][y]:
                    ret.append((x, y))
        return ret

    def get_path(self) -> tuple[int, list[tuple[int, int]]]:
        if self.path_limit:
            return self.id, single_agent_planner_v2.pad_path(self.planned_path, self.path_limit)
        else:
            return self.id, self.planned_path

    def check_collisions(self, paths: list[tuple[int, list[tuple[int, int]]]]):
        collision_list = []
        for path in paths:
            collision = collisions.detect_collision(self.id, path[0], self.planned_path, path[1])

            if collision:
                collision_list.append(collision)
                found = False
                for c in self.collision_memory:
                    if c == collision:
                        found = True
                        break
                if found:
                    self.repeat = collision
                else:
                    self.collision_memory.append(collision)
        return collision_list

    def move(self) -> tuple[int, list[tuple[int, int]]]:
        # clear memory
        self.message_memory = [self.message]
        self.collision_memory = []
        self.repeat = None

        # update constraints for new timestep
        for c in self.global_constraints:
            c.step -= 1
            if c.step <= 0:
                self.global_constraints.remove(c)

        # update path
        self.path.append(self.pos)
        self.pos = single_agent_planner_v2.get_location(self.planned_path, 1)  # update pos to position of next timestep

        self.planned_path = self.planned_path[min(1, len(self.planned_path) - 1):]
        return self.get_path()

    def resolve_collisions(self,
                           messages: list[tuple[tuple[int, int], tuple[int, int], int, int]]
                           ) -> tuple[int, list[tuple[int, int]]]:
        for message in messages:
            found = False
            for i, mem in enumerate(self.message_memory):
                if mem[0] == message[0]:
                    self.message_memory[i] = message
                    found = True
                    break
            if not found:
                self.message_memory.append(message)

        restrictions = sorted(self.message_memory, key=lambda x: x[2], reverse=True)
        idx = 0
        for i, restriction in enumerate(restrictions):
            if restriction[3] == self.id:
                idx = i
                break

        if self.repeat:
            for mem in self.message_memory:
                if self.repeat.agent_1 == mem[3]:
                    if self.message[2] < mem[2] or (self.message[2] == mem[2] and self.id < mem[3]):
                        self.global_constraints.append(self.repeat.standard_splitting()[0])

        for c in self.global_constraints:
            c.agent = idx

        solver = self.solver(self.my_map, [a[0] for a in restrictions], [a[1] for a in restrictions], self.score_func,
                             self.heuristics_func, printing=False, **self.kwargs)
        result = solver.find_solution(self.global_constraints)
        self.planned_path = result[idx]
        return self.get_path()


def run(agent_id: int,
        conn: multiprocessing.connection.Connection,
        start: tuple[int, int],
        goal: tuple[int, int],
        view_size: int,
        path_limit: int,
        my_map: list[list[bool]],
        heuristics_func: abc.Callable[[list[list[bool]], tuple[int, int]], dict[tuple[int, int], int]],
        score_func: abc.Callable[[list[list[tuple[int, int]]]], int],
        solver: type[base_solver.BaseSolver],
        **kwargs) -> None:
    #print(f"Init agent {agent_id}")
    agent = DistributedAgent(my_map, start, goal, view_size, path_limit, agent_id, heuristics_func, score_func, solver, **kwargs)
    while True:
        message = conn.recv()
        if message == "terminate":
            break
        elif message == "finished":
            conn.send(agent.finished)
        elif message == "view":
            conn.send((agent.id, agent.get_view()))
        elif message == "path":
            conn.send(agent.get_path())
        elif message == "collision":
            paths = conn.recv()
            conn.send((agent.id, agent.check_collisions(paths)))
        elif message == "move":
            conn.send((agent.id, agent.move()))
        elif message == "result":
            conn.send(agent.path)
        elif message == "message":
            conn.send(agent.message)
        elif message == "resolve":
            messages = conn.recv()
            conn.send((agent.id, agent.resolve_collisions(messages)))
        else:
            raise ValueError("Unknown message")
