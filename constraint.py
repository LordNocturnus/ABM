import collections.abc as abc
import typing


class PositionConstraint:

    def __init__(self, positive: bool, agent: int, loc: abc.Sequence[int, int], step: int) -> None:
        self.positive = positive
        self.agent = agent
        self.loc = loc
        self.step = step

    def compile_constraint(self, agent: int) -> "PositionConstraint":
        if agent == self.agent:
            return self
        elif self.positive:
            return PositionConstraint(False, agent, self.loc, self.step)


class EdgeConstraint:

    def __init__(self, positive: bool, agent: int, loc: abc.MutableSequence[abc.Sequence[int, int]], step: int) -> None:
        self.positive = positive
        self.agent = agent
        self.loc = loc
        self.step = step

    def compile_constraint(self, agent: int) -> typing.Optional[typing.Union[abc.Sequence["PositionConstraint"], "EdgeConstraint"]]:
        if agent == self.agent:
            if self.positive:
                return (
                    PositionConstraint(True, self.agent, self.loc[0], self.step - 1),
                    PositionConstraint(True, self.agent, self.loc[1], self.step)
                )
            else:
                return self
        elif self.positive:
            return (
                PositionConstraint(False, agent, self.loc[0], self.step - 1),
                PositionConstraint(False, agent, self.loc[1], self.step)
            )


