"""
This file contains the DistributedAgent class that can be used to implement individual planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""

from collections import abc
import multiprocessing
from multiprocessing import connection
import numpy as np
import numpy.typing as npt
import math

import collisions
import single_agent_planner
import base_solver
import view


class DistributedAgent(object):
    """"""

    def __init__(self,
                 my_map: npt.NDArray[bool],
                 start: tuple[int, int],
                 goal: tuple[int, int],
                 view_size: int,
                 path_limit: int,
                 agent_id: int,
                 heuristics_func: abc.Callable[[npt.NDArray[bool], tuple[int, int]], dict[tuple[int, int], int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int],
                 solver: type[base_solver.BaseSolver],
                 **kwargs
                 ) -> None:
        """
        """
        self.my_map = my_map
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
        self.path = [start]

        ## Initial Path finding procedure
        planned_path = single_agent_planner.a_star(my_map,
                                                   self.path[-1],
                                                   self.goal,
                                                   self.heuristics_func(self.my_map, self.goal),
                                                   self.id,
                                                   self.global_constraints)
        if planned_path is None:
            raise ValueError('No solutions')
        else:
            self.planned_path = planned_path[1:]

        self.message_memory = [self.message]
        self.collision_memory = []
        self.repeat = None

    @property
    def finished(self) -> bool:
        return self.path[-1] == self.goal

    @property
    def message(self) -> tuple[tuple[int, int], tuple[int, int], int, int]:
        return self.path[-1], self.goal, len(self.planned_path), self.id

    def get_view(self) -> list[tuple[int, int]]:
        """
            returns every coordinate visible to this agent
        """
        return view.fov_blocking(self.path[-1], self.view_size, self.my_map)

    def get_path(self) -> tuple[int, list[tuple[int, int]]]:
        if self.path_limit:
            return self.id, single_agent_planner.pad_path(self.planned_path, self.path_limit)
        else:
            return self.id, self.planned_path

    def check_collisions(self, paths: list[tuple[int, list[tuple[int, int]]]]):
        collision_list = []
        for path in paths:
            collision = collisions.detect_collision(self.id,
                                                    path[0],
                                                    single_agent_planner.pad_path(self.planned_path,
                                                                                  self.path_limit),
                                                    path[1])

            if collision:
                collision.step += 1
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

        if math.sqrt((self.path[-1][0] - self.planned_path[0][0]) ** 2 +
                     (self.path[-1][1] - self.planned_path[0][1]) ** 2) > 1:
            raise ValueError("Teleporting detected")

        # update constraints for new timestep
        for c in self.global_constraints:
            c.step -= 1
            if c.step <= 0:
                self.global_constraints.remove(c)

        # update path
        self.path.append(single_agent_planner.get_location(self.planned_path, 0))

        self.planned_path = self.planned_path[min(1, len(self.planned_path) - 1):]

        # clear memory
        self.message_memory = [self.message]
        self.collision_memory = []
        self.repeat = None
        return self.get_path()

    def resolve_collisions(self,
                           messages: list[tuple[tuple[int, int], tuple[int, int], int, int]]
                           ) -> tuple[int, list[tuple[int, int]]]:
        for message in messages:
            found = False
            for i, mem in enumerate(self.message_memory):
                if mem[3] == message[3]:
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
        self.planned_path = result[idx][min(1, len(result[idx]) - 1):]

        #if self.id == 2:
        #    print(self.id, "after planning ", self.path, self.planned_path)
        #    print("debug")

        return self.get_path()


def run(agent_id: int,
        conn: multiprocessing.connection.Connection,
        start: tuple[int, int],
        goal: tuple[int, int],
        view_size: int,
        path_limit: int,
        my_map: npt.NDArray[bool],
        heuristics_func: abc.Callable[[npt.NDArray[bool], tuple[int, int]], dict[tuple[int, int], int]],
        score_func: abc.Callable[[list[list[tuple[int, int]]]], int],
        solver: type[base_solver.BaseSolver],
        **kwargs) -> None:
    agent = DistributedAgent(my_map, start, goal, view_size, path_limit, agent_id, heuristics_func, score_func, solver, **kwargs)
    while True:
        try:
            message = conn.recv()
        except EOFError:
            break
        if message == "terminate":
            break
        elif message == "finished":
            conn.send(agent.finished)
        elif message == "view":
            conn.send((agent.id, agent.get_view()))
        elif message == "path":
            conn.send(agent.get_path())
        elif message == "collision":
            try:
                paths = conn.recv()
            except EOFError:
                break
            conn.send((agent.id, agent.check_collisions(paths)))
        elif message == "move":
            conn.send((agent.id, agent.move()))
        elif message == "result":
            conn.send(agent.path)
        elif message == "message":
            conn.send(agent.message)
        elif message == "resolve":
            messages = conn.recv()
            try:
                conn.send((agent.id, agent.resolve_collisions(messages)))
            except BrokenPipeError:
                break
        else:
            raise ValueError("Unknown message")
