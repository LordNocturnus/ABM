import typing
import constraints
import utils

from single_agent_planner_v2 import compute_heuristics, a_star, get_location, get_sum_of_cost


class Collision:

    def __init__(self,
                 agent_0: int,
                 agent_1: int,
                 step: int,
                 loc_0: tuple[int, int],
                 loc_1: typing.Optional[tuple[int, int]] = None) -> None:
        self.agent_0 = agent_0
        self.agent_1 = agent_1
        self.step = step
        self.loc_0 = loc_0
        self.loc_1 = loc_1

    def standard_splitting(self) -> tuple[constraints.Constraint, constraints.Constraint]:
        ##############################
        # Task 3.2: Return a list of (two) constraints to resolve the given collision
        #           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
        #                            specified timestep, and the second constraint prevents the second agent to be at the
        #                            specified location at the specified timestep.
        #           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
        #                          specified timestep, and the second constraint prevents the second agent to traverse the
        #                          specified edge at the specified timestep
        if self.loc_1:  # Edge collision
            return (constraints.Constraint(False, self.agent_0, self.step, self.loc_0, self.loc_1),
                    constraints.Constraint(False, self.agent_1, self.step, self.loc_1, self.loc_0))
        return (constraints.Constraint(False, self.agent_0, self.step, self.loc_0),
                constraints.Constraint(False, self.agent_1, self.step, self.loc_0))

    def disjoint_splitting(self, rng=utils.RNG) -> tuple[constraints.Constraint, constraints.Constraint]:
        ##############################
        # Task 4.1: Return a list of (two) constraints to resolve the given collision
        #           Vertex collision: the first constraint enforces one agent to be at the specified location at the
        #                            specified timestep, and the second constraint prevents the same agent to be at the
        #                            same location at the timestep.
        #           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
        #                          specified timestep, and the second constraint prevents the same agent to traverse the
        #                          specified edge at the specified timestep
        #           Choose the agent randomly
        agent = rng.choice((self.agent_0, self.agent_1))
        if self.loc_1:  # Edge collision
            return (constraints.Constraint(True, agent, self.step, self.loc_0, self.loc_1),
                    constraints.Constraint(False, agent, self.step, self.loc_0, self.loc_1))
        return (constraints.Constraint(True, agent, self.step, self.loc_0),
                constraints.Constraint(False, agent, self.step, self.loc_0))

    def __str__(self):
        if self.loc_1:
            return f"Edge Collision of agent {self.agent_0} and agent {self.agent_1} at timestep {self.step} between {self.loc_0} and {self.loc_1}\n"
        return f"Vertex collision of agent {self.agent_0} and agent {self.agent_1} at timestep {self.step} at location {self.loc_0}\n"

    def __repr__(self):
        return self.__str__()


def detect_collision(agent_0: int,
                     agent_1: int,
                     path_0: list[tuple[int, int]],
                     path_1: list[tuple[int, int]]) -> typing.Optional[Collision]:

    ##############################
    # Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
    #           There are two types of collisions: vertex collision and edge collision.
    #           A vertex collision occurs if both robots occupy the same location at the same timestep
    #           An edge collision occurs if the robots swap their location at the same timestep.
    #           You should use "get_location(path, t)" to get the location of a robot at time t.
    for i in range(max(len(path_0), len(path_1))):
        if get_location(path_0, i) == get_location(path_1, i):
            return Collision(agent_0, agent_1, i, get_location(path_0, i))
        elif get_location(path_0, i) == get_location(path_1, i + 1) and \
                get_location(path_0, i + 1) == get_location(path_1, i):
            return Collision(agent_0, agent_1, i + 1, get_location(path_0, i), get_location(path_0, i + 1))
    return None


def detect_collisions(paths: list[list[tuple[int, int]]]) -> dict[(int, int), Collision]:
    ##############################
    # Task 3.1: Return a list of first collisions between all robot pairs.
    #           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
    #           causing the collision, and the timestep at which the collision occurred.
    #           You should use your detect_collision function to find a collision between two robots.
    res: dict[(int, int), Collision] = dict()
    for a0, p0 in enumerate(paths[:-1]):
        for a1, p1 in enumerate(paths[a0 + 1:]):
            collision = detect_collision(a0, a0 + a1 + 1, p0, p1)
            if collision:
                res[(a0, a0 + a1 + 1)] = collision
    return res