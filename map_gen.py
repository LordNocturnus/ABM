import os

import numpy as np  # type: ignore
import numpy.typing as npt  # type: ignore
import utils
import os


class MapGenerator(object):

    def __init__(self, path: str, seed: int = 0) -> None:
        with open(path, "r") as f:
            string_map = f.readlines()
        list_map = []
        for i, line in enumerate(string_map):
            list_map.append([*line][:-1])
        array_map = np.array(list_map)
        self.map = np.array(array_map == "@", dtype=int)
        self.rng = np.random.default_rng(seed)
        xrange = np.arange(0, self.map.shape[0])
        yrange = np.arange(0, self.map.shape[1])
        xgrid, ygrid = np.meshgrid(yrange, xrange)
        self.candidates = utils.pos_to_prime(xgrid, ygrid)[self.map == 0]
        self.str_output = ""

    def generate(self, agents: int = 7) -> tuple[npt.NDArray[int], list[tuple[int, int]], list[tuple[int, int]]]:
        starts_x, starts_y = utils.prime_to_pos(self.rng.choice(self.candidates, agents, replace=False))

        goals_x, goals_y = utils.prime_to_pos(self.rng.choice(self.candidates, agents, replace=False))

        starts = [(starts_y[i], starts_x[i]) for i in range(agents)]
        goals = [(goals_y[i], goals_x[i]) for i in range(agents)]

        return self.map, starts, goals


if __name__ == "__main__":
    test = MapGenerator("maps/assignment_1.map")
    print(test.generate())
