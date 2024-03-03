import numpy as np
from globals import PRIMEX, PRIMEY


class MapGenerator(object):

    def __init__(self, path, seed=0):
        with open(path, "r") as file:
            map = file.readlines()
        for i, line in enumerate(map):
            map[i] = [*line][:-1]
        map = np.asarray(map)
        self.map = np.asarray(map == ".", dtype=int)
        self.rng = np.random.default_rng(seed)
        xrange = np.arange(0, self.shape[0])
        yrange = np.arange(0, self.shape[1])
        xgrid, ygrid = np.meshgrid(yrange, xrange)
        self.candidates = (xgrid * PRIMEX + ygrid * PRIMEY)[self.map == 1]

    def generate(self, agents=7):
        starts = self.rng.choice(self.candidates, agents)
        starts_y = (starts % PRIMEX) / 2
        starts_x = (starts - starts_y * PRIMEY) / PRIMEX

        goals = self.rng.choice(self.candidates, agents)
        goals_y = (goals % PRIMEX) / 2
        goals_x = (goals - goals_y * PRIMEY) / PRIMEX

        agents = np.transpose(np.asarray([starts_x, starts_y, goals_x, goals_y]))
        ret = self.lines
        ret.append(f"{len(agents)}\n")
        for agent in agents:
            ret.append(f"{int(agent[0])} {int(agent[1])} {int(agent[2])} {int(agent[3])}\n")
        return "".join(ret)

    @property
    def shape(self):
        return self.map.shape

    @property
    def lines(self):
        ret = list()
        ret.append(f"{self.shape[0]} {self.shape[1]}\n")
        for line in self.map:
            res = np.empty(line.shape, dtype=str)
            res[line == 0] = "@"
            res[line == 1] = "."
            ret.append(" ".join(res) + "\n")
        return ret



if __name__ == "__main__":
    test = MapGenerator("maps/assignment_1.map")
    print(test.generate())
