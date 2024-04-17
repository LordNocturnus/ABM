import collections.abc as abc
import typing


class Constraint:
    """
        Class used to communicate different types of path restrictions. Can be either a Vertex or Edge constraint where
        vertex refers to a location while edge refers to a move between two adjacent locations. The constraint can be
        positive forcing the agent to occupy the specified location at the specified timestep or perform the specified
        move at the specified timestep while a negative constraint forbids it. Lastly positional constraints can be
        infinite meaning they are enforced from the provided timestep onwards.

    :param agent:       {int}   Agent affected by this constraint
    :param edge:        {bool}  property returning if this constraint is an edge or a vertex constraint
    :param infinite:    {bool}  flag for infinite constraint
    :param loc_1:       {tuple} location of this constraint
    :param loc_2:       {tuple} optional second location of this constraint that is only present if it is a edge
                                constraint
    :param positive:    {bool}  flag for enforcing or forbidding of location/move
    :param step:        {int}   timestep at which to apply this constraint
    """

    def __init__(self,
                 positive: bool,
                 agent: int,
                 step: int,
                 loc_1: typing.Optional[abc.Sequence[int]],
                 loc_2: typing.Optional[abc.Sequence[int]] = None,
                 infinite: bool = False) -> None:
        """
            Initialization function for the Constraint class. It check if the first location is none or if an edge
            collision is attempted to be made infinite and raises a ValueError if either occur

        :param agent:       {int}   Agent affected by this constraint
        :param infinite:    {bool}  flag for infinite constraint
        :param loc_1:       {tuple} location of this constraint
        :param loc_2:       {tuple} optional second location of this constraint that is only present if it is a edge
                                    constraint
        :param positive:    {bool}  flag for enforcing or forbidding of location/move
        :param step:        {int}   timestep at which to apply this constraint

        :raise:                     ValueError
        :raise:                     ValueError
        """
        self.positive = positive
        self.agent = agent
        if loc_1 is None:
            raise ValueError("Constraint can not have 'None' at location 0")
        self.loc_1 = loc_1
        self.loc_2 = loc_2
        if self.edge and infinite:
            raise ValueError("Edge constraints can not be infinite")
        self.step = step
        self.infinite = infinite

    @property
    def edge(self) -> bool:
        """
            property returning if this constraint is an edge or a vertex constraint

        :return:    {bool}  if location two exists it is and edge constraint
        """
        return self.loc_2 is not None

    def compile_constraint(self, agent: int) -> abc.Iterator["Constraint"]:
        """
            Converts this constraint that might not apply to the given agent to constraint(-s) that apply to the given
            agent. If the given agent is the same as the constraints agent it splits edge constraints into two vertex
            constraints or returns it self.
            If the agent is not the same then this constraint only needs to be considered if it is positive. Then it
            splits edge constraints into three negative constraints for the given agent two for the locations of the
            edge constraints and a edge constraint traversing the locations in reversed order otherwise if it is a
            vertex constraint it returns a negative vertex constraint for given agent

                :param agent:   {int}           Agent for whom to apply the constraints

                :yield:         {Constraint}    Positive vertex constraint at location one applied at the previous
                                                timestep
                :yield:         {Constraint}    Positive vertex constraint at location two applied at the current
                                                timestep
                :yield:         {Constraint}    No change necessary
                :yield:         {Constraint}    Negative vertex constraint at location one applied at the previous
                                                timestep
                :yield:         {Constraint}    Negative vertex constraint at location two applied at the current
                                                timestep
                :yield:         {Constraint}    Negative edge constraint at the same timestep with reversed locations
                :yield:         {Constraint}    Negative vertex constraint at location one applied at the current
                                                timestep
        """
        if agent == self.agent:
            if self.positive and self.edge:
                yield Constraint(True, agent, self.step - 1, self.loc_1)
                yield Constraint(True, agent, self.step, self.loc_2)
            else:
                yield self
        elif self.positive:
            if self.edge:
                yield Constraint(False, agent, self.step - 1, self.loc_1)
                yield Constraint(False, agent, self.step, self.loc_2)
                yield Constraint(False, agent, self.step, self.loc_2, self.loc_1)
            else:
                yield Constraint(False, agent, self.step, self.loc_1, infinite=self.infinite)

    def __str__(self) -> str:
        """
            Overwrites the str methode for the Constraint class. When calling str(Constraint) an adapted output will be
            provided.

            :return:    {str}   String output describing the edge constraint.
            :return:    {str}   String output describing the vertex constraint.
        """
        if self.positive:
            pos = "Positive"
        else:
            pos = "Negative"
        if self.loc_2:
            return f"{pos} edge Constraint of agent {self.agent} at timestep {self.step} between {self.loc_1} and {self.loc_2}\n"
        return f"{pos} vertex Constraint of agent {self.agent} at timestep {self.step} at location {self.loc_1}\n"

    def __repr__(self) -> str:
        """
            Overwrites the repr methode for the Constraint class.

        :return:    {str}   String output describing the type of constraint, using .__str__()
        """
        return self.__str__()


class ConstraintTable:
    """
        Class used to sort and handle Constraints applied to a given agent.

        :param finite_constraints:      {int}   list of all constraints applied to the given agent that have a finite
                                                duration sorted by time step at which they occur
        :param infinite_constraints:    {bool}  list of all constraints applied to the given agent that have a infinite
                                                duration sorted by time step at which they start occurring
        :param is_infinite:             {bool}  indicator property showing if any infinite constraints are present
    """

    def __init__(self, constraints: list[Constraint], agent: int) -> None:
        """
            Initialization function for the ConstraintTable class. Iterates through all provided constraints and uses
            Constraint.compile_constraint

        :param constraints: {list}  list of all constraints currently in scope for the pathfinding potentially not all
                                    applying to the given agent
        :param agent:       {int}   agent for which to store the required constraints
        """
        self.finite_constraints = []
        self.infinite_constraints = []
        for constraint in constraints:
            for c in constraint.compile_constraint(agent):
                if c.infinite:
                    self.infinite_constraints.append(c)
                else:
                    self.finite_constraints.append(c)
        self.finite_constraints.sort(key=lambda x: x.step)
        self.infinite_constraints.sort(key=lambda x: x.step)

    def is_constrained(self, current_loc: tuple[int, int], next_loc: tuple[int, int], step: int) -> bool:
        if step < len(self):
            for c in self.finite_constraints:
                if c.step < step:
                    continue
                elif c.step > step:
                    break
                if c.positive:  # positive constraint
                    if c.loc_1 != next_loc:
                        return True
                elif c.loc_2 is None:  # negative vertex constrain
                    if c.loc_1 == next_loc:
                        return True
                elif c.loc_1 == current_loc and c.loc_2 == next_loc:  # negative edge constraint
                    return True
        if self.is_infinite and step >= self.infinite_constraints[0].step:
            for c in self.infinite_constraints:
                if c.step > step:
                    break
                if c.loc_1 == next_loc:
                    return True
        return False

    @property
    def is_infinite(self):
        return len(self.infinite_constraints) != 0

    def __len__(self) -> int:
        try:
            return self.finite_constraints[-1].step + 1
        except IndexError:
            return 0
