import collections.abc as abc
import typing


class Constraint:

    def __init__(self,
                 positive: bool,
                 agent: int,
                 step: int,
                 loc_1: abc.Sequence[int] | None,
                 loc_2: abc.Sequence[int] | None = None,
                 duration: int = 1) -> None:
        self.positive = positive
        self.agent = agent
        if loc_1 is None:
            raise ValueError("Constraint can not have 'None' at location 0")
        self.loc_1 = loc_1
        self.loc_2 = loc_2
        if self.edge and duration != 1:
            raise ValueError("Edge constraints can not have a duration")
        self.step = step
        self.duration = duration

    @property
    def edge(self) -> bool:
        return self.loc_1 is not None

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
                yield Constraint(False, agent, self.step, self.loc_1, self.loc_2)
            else:
                yield Constraint(False, agent, self.step, self.loc_1, duration=self.duration)
