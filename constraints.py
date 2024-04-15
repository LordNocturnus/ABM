import collections.abc as abc
import typing


class Constraint:

    def __init__(self,
                 positive: bool,
                 agent: int,
                 step: int,
                 loc_1: typing.Optional[abc.Sequence[int]],
                 loc_2: typing.Optional[abc.Sequence[int]] = None,
                 infinite: bool = False) -> None:
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
        return self.loc_2 is not None

    def compile_constraint(self, agent: int) -> abc.Iterator["Constraint"]:
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
        if self.positive:
            pos = "Positive"
        else:
            pos = "Negative"
        if self.loc_2:
            return f"{pos} edge Constraint of agent {self.agent} at timestep {self.step} between {self.loc_1} and {self.loc_2}\n"
        return f"{pos} vertex Constraint of agent {self.agent} at timestep {self.step} at location {self.loc_1}\n"

    def __repr__(self) -> str:
        return self.__str__()


class ConstraintTable:

    def __init__(self, constraints: list[Constraint], agent: int) -> None:
        self.constraints = []
        for constraint in constraints:
            for c in constraint.compile_constraint(agent):
                self.constraints.append(c)
        self.constraints.sort(key=lambda x: x.step)

    def is_constrained(self, current_loc: tuple[int, int], next_loc: tuple[int, int], step: int) -> bool:
        for c in self.constraints:
            if c.step < step:
                continue
            elif c.step > step:
                break
            if c.positive: # positive constraint
                if c.loc_1 != next_loc:
                    return True
            elif c.loc_2 is None: # negative vertex constrain
                if c.loc_1 == next_loc:
                    return True
            elif c.loc_1 == current_loc and c.loc_2 == next_loc: # negative edge constraint
                return True
        return False

    def __len__(self) -> int:
        try:
            return self.constraints[-1].step + 1
        except IndexError:
            return 0
