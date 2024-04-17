"""
This file contains a placeholder for the DistributedPlanningSolver class that can be used to implement distributed planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
from collections import abc
import time as timer
import multiprocessing
from multiprocessing import connection

from single_agent_planner import compute_heuristics, get_sum_of_cost
from prioritized import PrioritizedPlanningSolver
import distributed_agent
import base_solver
import constraints


class DistributedPlanningSolver(base_solver.BaseSolver):
    """A distributed planner"""

    def __init__(self,
                 my_map: list[list[bool]],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int] = get_sum_of_cost,
                 heuristics_func: abc.Callable[
                     [list[list[bool]], tuple[int, int]],
                     dict[tuple[int, int], int]] = compute_heuristics,
                 printing: bool = True,
                 solver: type[base_solver.BaseSolver] = PrioritizedPlanningSolver,
                 view_size: int = -1,
                 path_limit: int = -1,
                 **kwargs) -> None:
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """
        super().__init__(my_map, starts, goals, score_func, heuristics_func, printing)
        self.solver = solver
        self.view_size = view_size
        self.path_limit = path_limit
        self.kwargs = kwargs

        self.visibility_map = dict()
        self.path_map = dict()
        self.collision_map = dict()
        self.agent_pos = self.starts

        self.processes: list[multiprocessing.Process] = []
        self.pipes: list[multiprocessing.connection.Connection] = []
        
    def find_solution(self, base_constraints: list[constraints.Constraint]) -> list[list[tuple[int, int]]]:
        """
        Finds paths for all agents from start to goal locations.
        
        Returns:
            result (list): with a path [(s,t), .....] for each agent.
        """
        # Initialize constants       
        start_time = timer.time()

        # initialize agents and communication paths
        for agent_id in range(self.num_of_agents):
            controller_conn, agent_conn = multiprocessing.Pipe()
            self.pipes.append(controller_conn)
            self.processes.append(multiprocessing.Process(target=distributed_agent.run,
                                                          args=[agent_id,
                                                                agent_conn,
                                                                self.starts[agent_id],
                                                                self.goals[agent_id],
                                                                self.view_size,
                                                                self.path_limit,
                                                                self.my_map,
                                                                self.heuristics_func,
                                                                self.score_func,
                                                                self.solver],
                                                          kwargs=self.kwargs))
            self.processes[-1].start()
            agent_conn.close()
            self.path_map[agent_id] = self.get_path(agent_id)

        while not all([self.get_finished(idx) for idx in range(self.num_of_agents)]):
            self.poll_view()
            self.poll_collisions()

            while len(self.collision_map) != 0:
                self.resolve_collisions()
                self.poll_collisions()

            self.instruct_move()

        result = []
        for agent_id in range(self.num_of_agents):
            result.append(self.get_result(agent_id))
            self.terminate_agent(agent_id)

        self.CPU_time = timer.time() - start_time

        # Print final output
        if self.printing:
            print("\n Found a solution! \n")
            print("CPU time (s):    {:.2f}".format(self.CPU_time))
            print("Sum of costs:    {}".format(self.score_func(result)))
            print(result)
        
        return result

    def terminate_agent(self, idx) -> None:
        self.pipes[idx].send("terminate")  # TODO: change to integer index
        self.pipes[idx].close()
        self.processes[idx].join()
        self.processes[idx].close()

    def get_finished(self, idx):
        self.pipes[idx].send("finished")  # TODO: change to integer index
        return self.pipes[idx].recv()

    def poll_view(self) -> None:
        self.visibility_map = dict()
        missing_view = []
        for p in self.pipes:
            p.send("view")  # TODO: change to integer index
            missing_view.append(p)

        while missing_view:
            for r in multiprocessing.connection.wait(missing_view):
                idx, fov = r.recv()
                visible = [a for a, pos in enumerate(self.agent_pos) if pos in fov and not a == idx]
                if len(visible) != 0:
                    self.visibility_map[idx] = visible
                missing_view.remove(r)

    def get_path(self, idx: int) -> tuple[list[tuple[int, int]], int]:
        self.pipes[idx].send("path")  # TODO: change to integer index
        return self.pipes[idx].recv()

    def poll_collisions(self) -> None:
        self.collision_map = dict()
        missing_collision = []
        for agent_id in self.visibility_map.keys():
            self.pipes[agent_id].send("collision")
            self.pipes[agent_id].send([self.path_map[a] for a in self.visibility_map[agent_id]])
            missing_collision.append(self.pipes[agent_id])

        while missing_collision:
            for r in multiprocessing.connection.wait(missing_collision):
                idx, collisions = r.recv()
                if len(collisions) != 0:
                    self.collision_map[idx] = collisions
                missing_collision.remove(r)

    def instruct_move(self) -> None:
        missing_move = []
        for p in self.pipes:
            p.send("move")  # TODO: change to integer index
            missing_move.append(p)

        while missing_move:
            for r in multiprocessing.connection.wait(missing_move):
                idx, path = r.recv()
                self.path_map[idx] = path
                missing_move.remove(r)

    def get_result(self, idx: int) -> list[tuple[int, int]]:
        self.pipes[idx].send("result")  # TODO: change to integer index
        return self.pipes[idx].recv()

    def get_message(self, idx: int) -> list[tuple[int, int]]:
        self.pipes[idx].send("message")  # TODO: change to integer index
        return self.pipes[idx].recv()

    def resolve_collisions(self) -> None:
        messages = dict()
        for agent_id in self.collision_map.keys():
            messages[agent_id] = [self.get_message(c.agent_1) for c in self.collision_map[agent_id]]
        missing_resolve = []
        for agent_id in self.collision_map.keys():
            self.pipes[agent_id].send("resolve")
            self.pipes[agent_id].send(messages[agent_id])
            missing_resolve.append(self.pipes[agent_id])

        while missing_resolve:
            for r in multiprocessing.connection.wait(missing_resolve):
                idx, path = r.recv()
                self.path_map[idx] = path
                missing_resolve.remove(r)

