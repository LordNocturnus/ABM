"""
This file contains a placeholder for the DistributedPlanningSolver class that can be used to implement distributed planning.

Code in this file is just provided as guidance, you are free to deviate from it.
"""
from collections import abc
import time as timer
import numpy as np
import numpy.typing as npt
import multiprocessing
from multiprocessing import connection

from single_agent_planner import compute_heuristics, get_sum_of_cost
from prioritized import PrioritizedPlanningSolver
import distributed_agent
import base_solver
import constraints


class DistributedPlanningSolver(base_solver.BaseSolver):
    """
        Class for solving multi agent pathfinding problems using distributed computing. The only purpose of this class
        is determining and facilitating which agent can and needs to communicate with which other agent.

    :param CPU_time:        {float}     Value to keep track of the cpu time required for the solver to complete the
                                        planning
    :param agent_pos:       {list}      List containing the current position of all agents
    :param collision_map:   {dict}      dictionary containing at each agents index the collisions of that agent with all
                                        other agents in his view
    :param my_map:          {list}      List of list of boolean, describing the map environment. True indicates a wall.
    :param starts:          {list}      List of starting positions for the agents. Given as list of tuple of integer,
                                        where each each tuple is of the following form (y, x)
                                        [(x1, y1), (x2, y2), ...]
    :param goals:           {list}      List of goal/ end positions for the agents. Given as list of tuple of integer,
                                        where each each tuple is of the following form (y, x)
                                        [(x1, y1), (x2, y2), ...]
    :param score_func:      {function}  Score function
    :param heuristics_func: {function}  Heuristics function
    :param printing:        {bool}      Variable to enable and disable printing within the model. This allows for the
                                        user to specify if they would like to receive the solver outcome after every run
                                        or not. True enables printing while false disables this behaviour.
    :param num_of_agents:   {int}       The number of agents within the environment. Extracted from the supplied goal or
                                        start positions.
    :param path_limit:      {int}       maximum number of steps that are being communicated by agents values smaller
                                        than one result in communication of the full path
    :param kwargs:          {dict}      arguments to pass along to the given solver
    :param path_map:        {dict}      dictionary containing the communicated path and the current length of the
                                        planned path of each agent at that agents index
    :param pipes:           {list}      List containing one the multiprocessing pipe that are used for bidirectional
                                        communication with the agents for each agent
    :param processes:       {list}      List containing the multiprocessing processes that are running the calculations
                                        for each agent
    :param solver:          {list}      chosen solver to be run by each agent to update their own path at every timestep
    :param view_size:       {int}       maximum distance at which an agent can see other agents
    :param visibility_map:  {dict}      dictionary containing at each agents index the indices of all other agents in
                                        view of that agent
    """

    def __init__(self,
                 my_map: npt.NDArray[bool],
                 starts: list[tuple[int, int]],
                 goals: list[tuple[int, int]],
                 score_func: abc.Callable[[list[list[tuple[int, int]]]], int] = get_sum_of_cost,
                 heuristics_func: abc.Callable[
                     [npt.NDArray[bool], tuple[int, int]],
                     dict[tuple[int, int], int]] = compute_heuristics,
                 printing: bool = True,
                 solver: type[base_solver.BaseSolver] = PrioritizedPlanningSolver,
                 view_size: int = -1,
                 path_limit: int = -1,
                 **kwargs) -> None:
        """
            Initialization function for DistributedPlanningSolver. Inherits from BaseSolver and then initializes all
            other parameters.

        :param my_map:          {list}      List of list of boolean, describing the map environment. True indicates a
                                            wall.
        :param starts:          {list}      List of starting positions for the agents. Given as list of tuple of
                                            integers, where each each tuple is of the following form (y, x)
        :param goals:           {list}      List of goal/ end positions for the agents. Given as list of tuple of
                                            integers, where each each tuple is of the following form (y, x)
        :param score_func:      {function}  Score function
        :param heuristics_func: {function}  Heuristics function
        :param printing:        {bool}      Variable to enable and disable printing within the model. This allows for
                                            the user to specify if they would like to receive the solver outcome after
                                            every run or not. True enables printing while false disables this behaviour.
        :param solver:          {list}      chosen solver to be run by each agent to update their own path at every
                                            timestep
        :param view_size:       {int}       maximum distance at which an agent can see other agents
        :param path_limit:      {int}       maximum number of steps that are being communicated by agents values smaller
                                        than one result in communication of the full path
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
            Main function for solving the multi agent path finding problem. It starts by initializing all agents as
            subprocesses each with a pipe to communicate. To ensure no accidental dangling pipes are present the agent
            side of the pipe is closed in the main process once it has been handed to the subprocess. Then it gathers
            the currently planned paths for each agent for communication in the future.
            After initialization of all agents it starts of a loop by polling all agents for their view and any
            collisions. If collisions are found it instructs all agents to repeatedly resolve collisions and poll for
            collisions until no collisions are left. Lastly all agents are instructed to move by one step.
            The above is repeated until all agents have reached their goal. After which the resulting path is requested
            from each agent and the agent subprocess is terminated.

        :param base_constraints:    {list}  List of list of boolean, describing the map environment. True indicates a
                                            wall.

        :return:                    {list}  Paths traversed by all agents
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

        s = 0

        while not all([self.get_finished(idx) for idx in range(self.num_of_agents)]):
            self.poll_view()
            self.poll_collisions()

            c = 0

            while len(self.collision_map) != 0:
                print(s, c, len(self.collision_map))
                for key in self.collision_map.keys():
                    print(key, self.collision_map[key])
                self.resolve_collisions()
                self.poll_collisions()
                c += 1

            self.instruct_move()
            s += 1

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

    def terminate_agent(self, idx: int) -> None:
        """
            sends the terminate command to the agent subprocess at the given index and then closes both the pipe and the
            agent

        :param idx: {int}   agent index
        """
        self.pipes[idx].send("terminate")
        self.pipes[idx].close()
        self.processes[idx].join()
        self.processes[idx].close()

    def get_finished(self, idx):
        """
            sends the finished request to the agent subprocess at the given index and returns the response

        :param idx: {int}   agent index

        :return:    {bool}  has agent reached its goal position
        """
        self.pipes[idx].send("finished")
        return self.pipes[idx].recv()

    def poll_view(self) -> None:
        """
            sends the view command to each agent and stores a reference to each pipe in missing_view then awaits a
            response on any of the pipes containing the agents index and a list of tuples which are the vertices the
            agent can see. These vertices are then compared to the positions of all agents and if an agents position is
            in the list of visible vertices then its id is added to the visibility map at the current agents index
        """
        self.visibility_map = dict()
        missing_view = []
        for p in self.pipes:
            p.send("view")
            missing_view.append(p)

        while missing_view:
            for r in multiprocessing.connection.wait(missing_view):
                idx, fov = r.recv()
                visible = [a for a, pos in enumerate(self.agent_pos) if pos in fov and not a == idx]
                if len(visible) != 0:
                    self.visibility_map[idx] = visible
                missing_view.remove(r)

    def get_path(self, idx: int) -> tuple[list[tuple[int, int]], int]:
        """
            sends the path request to the agent subprocess at the given index and returns the response

        :param idx: {int}   agent index

        :return:    {list}  planned path of the agent up to path limit length
        """
        self.pipes[idx].send("path")
        return self.pipes[idx].recv()

    def poll_collisions(self) -> None:
        """
            clears the collision map and then sends the collision command and then a list of all paths for agents in
            view to each agent that is able to see other agents. Then awaits a response containing the corresponding
            agent index and the list of all collisions that occur both are then used to update the collision map
        """
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
        """
            sends the move command to each agent and stores a reference to each pipe in missing_move then awaits a
            response on any of the pipes containing the agents index and the updated path which are then used to update
            the path map
        """
        missing_move = []
        for i, p in enumerate(self.pipes):
            self.agent_pos[i] = self.path_map[i][1][1]
            p.send("move")
            missing_move.append(p)

        while missing_move:
            for r in multiprocessing.connection.wait(missing_move):
                idx, path = r.recv()
                self.path_map[idx] = path
                missing_move.remove(r)

    def get_result(self, idx: int) -> list[tuple[int, int]]:
        """
            sends the result request to the agent subprocess at the given index and returns the response

        :param idx: {int}   agent index

        :return:    {list}  complete path of the agent from start to current position
        """
        self.pipes[idx].send("result")
        return self.pipes[idx].recv()

    def get_message(self, idx: int) -> tuple[tuple[int, int], tuple[int, int], int, int]:
        """
            sends the message request to the agent subprocess at the given index and returns the response

        :param idx: {int}   agent index

        :return:    {tuple} tuple containing the current agent position, its goal location, its current planned path
                            length and its id
        """
        self.pipes[idx].send("message")
        return self.pipes[idx].recv()

    def resolve_collisions(self) -> None:
        """
            starts by collecting the messages from all agents and then sends to every agent that is colliding with any
            other agent a list of messages form all agents it is colliding with after sending the resolve command to it.
            Then waits for a response from each agent which is then used to update the path map
        """
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

