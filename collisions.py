import typing
import constraints
import utils
import numpy.typing as npt  # type: ignore
import numpy as np

from single_agent_planner import get_location


class Collision:
    """
        Class to represent Collisions. Utilised heavily within the collision based search (cbs) algorithm. It can
        two resolve collisions to methods can be made use of. Standard splitting and disjoint splitting. In standard
        splitting the agents are prevented from being at a certain location at a certain timestep. While in disjoint 
        splitting the constraint forces one of the two agents to be and not be (Two constraints) at the specified
        location at a certain time. In both cases a decision tree is being created, trough which is being iterated to
        find a solution.
    
    :param agent_0: {int}   The unique identifier of agent 0
    :param agent_1: {int}   The unique identifier of agent 1
    :param step:    {int}   Time step of collision
    :param loc_0:   {tuple} Location at the time of collision
    :param loc_1:   {tuple} Optional location at the time of collision to fully define edge collisions 
                            together with loc_0
    :param edge:    {bool}  Property, True if the collision is an edge, else false
    """

    def __init__(self,
                 agent_0: int,
                 agent_1: int,
                 step: int,
                 loc_0: tuple[int, int],
                 loc_1: typing.Optional[tuple[int, int]] = None) -> None:
        """
            Initialise collision class required for the cbs solver
        
        :param agent_0: {int}   The unique identifier of agent 0
        :param agent_1: {int}   The unique identifier of agent 1
        :param step:    {int}   Time step of collision
        :param loc_0:   {tuple} Location at the time of collision
        :param loc_1:   {tuple} Optional location at the time of collision to fully define edge collisions 
                                together with loc_0
        """
        
        self.agent_0 = agent_0
        self.agent_1 = agent_1
        self.step = step
        self.loc_0 = loc_0
        self.loc_1 = loc_1

    def standard_splitting(self) -> tuple[constraints.Constraint, constraints.Constraint]:
        """
            Standard splitting for the creation of constraints for the cbs algorithm

        :return:    {constraints.Constraint, constraints.Constraint}    Negative edge constraint first for agent_0 then
                                                                        for agent_1 each of which independently resolves
                                                                        this collision
        :return:    {constraints.Constraint, constraints.Constraint}    Negative vertex constraint first for agent_0
                                                                        then for agent_1 each of which independently
                                                                        resolves this collision
        """
        
        if self.edge:  # Edge collision
            return (constraints.Constraint(False, self.agent_0, self.step, self.loc_0, self.loc_1),
                    constraints.Constraint(False, self.agent_1, self.step, self.loc_1, self.loc_0))
        return (constraints.Constraint(False, self.agent_0, self.step, self.loc_0),
                constraints.Constraint(False, self.agent_1, self.step, self.loc_0))

    def disjoint_splitting(self, rng: np.random._generator = utils.RNG) -> tuple[constraints.Constraint, constraints.Constraint]:
        """
            Disjoint splitting for the creation of constraints for the cbs algorithm. Makes use of an rng to determine
            on which agent the constraints should be enforced.
        
        :param rng: {utils.RNG}                                         RNG generator to be utilised.

        :return:    {constraints.Constraint, constraints.Constraint}    A positive and negative edge constrain for the
                                                                        selected agent
        :return:    {constraints.Constraint, constraints.Constraint}    A positive and negative vertex constrain for the
                                                                        selected agent
        """
        agent = rng.choice((self.agent_0, self.agent_1))
        
        if self.edge:  # Edge collision
            return (constraints.Constraint(True, agent, self.step, self.loc_0, self.loc_1),
                    constraints.Constraint(False, agent, self.step, self.loc_0, self.loc_1))
        return (constraints.Constraint(True, agent, self.step, self.loc_0),
                constraints.Constraint(False, agent, self.step, self.loc_0))

    @property
    def edge(self) -> bool:
        """
            Property to determine if the collision is an edge collision or not
        
        :return:    {bool}  returns True if self.loc_1 exists else False is returned, indicating the collision is 
                            a vertex collision.
        """
        return self.loc_1 is not None

    def __str__(self) -> str:
        """
            Overwrites the str methode for the Collision class. When calling str(Collisions) an adapted output will be
            provided.
        
        :return:    {str}   String output describing the edge collision.
        :return:    {str}   String output describing the vertex collision.
        """
        if self.loc_1:
            return f"Edge Collision of agent {self.agent_0} and agent {self.agent_1} at timestep {self.step} between {self.loc_0} and {self.loc_1}\n"
        return f"Vertex collision of agent {self.agent_0} and agent {self.agent_1} at timestep {self.step} at location {self.loc_0}\n"

    def __repr__(self) -> str:
        """
            Overwrites the repr methode for the Collision class. 
        
        :return:    {str}   String output describing the type of collision, using .__str__()
        """
        return self.__str__()

    def __eq__(self, other: "Collision") -> bool:
        """
            Overwrites the equal methode for the Collision class. Allowing for easier comparison between two Collision
            objects. When utilising an if statement no further detail needs to be provided since this methode overwrites
            the typical behaviour. And will output True when put into an if statement to check if the Collision is a 
            collision or if two collisions needs to be compared.
        
        :param other:   {Collision} A second collision object, to compare with
        
        :return:        {bool}      Returns True if the other collision has the same agents, locations and timestep
        """
        return (self.agent_0 == other.agent_0 and
                self.agent_1 == other.agent_1 and
                self.loc_0 == other.loc_0 and
                self.loc_1 == other.loc_1 and
                self.step == other.step)


def detect_collision(agent_0: int,
                     agent_1: int,
                     path_0: list[tuple[int, int]],
                     path_1: list[tuple[int, int]]) -> typing.Optional[Collision]:
    """
        Function to detect the first collision (indexed by time), between two agents paths. Required function of the
        main function detect_collisions.

    :param agent_0: {int}       The unique identifier of agent 0
    :param agent_1: {int}       The unique identifier of agent 1
    :param path_0:  {list}      The path of agent 0
    :param path_1:  {list}      The path of agent 1

    :return:        {Collision} Collision object, containing the details of the identified vertex collision.
    :return:        {Collision} Collision object, containing the details of the identified edge collision.
    :return:        {None}      No collision has been found
    """
    for i in range(max(len(path_0), len(path_1))):

        # Vertex 
        if get_location(path_0, i) == get_location(path_1, i):
            return Collision(agent_0, agent_1, i, get_location(path_0, i))
        # Edge
        elif get_location(path_0, i) == get_location(path_1, i + 1) and \
                get_location(path_0, i + 1) == get_location(path_1, i):
            return Collision(agent_0, agent_1, i + 1, get_location(path_0, i), get_location(path_0, i + 1))
    
    return None


def detect_collisions(paths: list[list[tuple[int, int]]]) -> dict[tuple[int, int], Collision]:
    """
        Function to generate a list of first collisions between all agent pairs
    
    :param paths:   {list}  List of list of tuple of two integer. Describing the paths of the various agents, located
                            within the environment.

    :return:        {dict}  Dictionary containing the identified first collisions between all agent pairs (if a 
                            collision) exists. The indexing used in this dictionary are tuples of two agent ids which
                            correspond to the agents that are causing the collision at that index.
    """
    res: dict[tuple[int, int], Collision] = dict()
    
    # Loop over all possible agent pairs
    for a0, p0 in enumerate(paths[:-1]):
        for a1, p1 in enumerate(paths[a0 + 1:]):
            
            collision = detect_collision(a0, a0 + a1 + 1, p0, p1)
            
            # Check if collision exists
            if collision:
                res[(a0, a0 + a1 + 1)] = collision
    return res
