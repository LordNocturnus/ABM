import numpy as np  # type: ignore
import numpy.typing as npt  # type: ignore
import utils
import os


class MapGenerator(object):
    """
        Map generator to both load the map and create various random test scenarious with agents located throughout
        various locations within the map. Utelising prime number ...
        Point of discussion meeting 15-4-24 // If time have various random generator for unique cases

    :param map:         {np.NDArray}    Environment map, where 1 indicates a wall, and 0 indicates walkable space.

    :param rng:         {generator}     Random number generator generator object, required to set the seed of the rng
                                        process.

    :param candidates:  {np.NDArray}    

    :param str_output:  {str}           Do we even need this anymore ??
    """

    def __init__(self, path: str, seed: int = 0) -> None:
        """
            Initialise map geneator object.
        
        :param path:    {str}   Path to the map file.

        :param seed:    {int}   Set the seed of the rng process.

        :return:        {None}  -
        """
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
        """
            Generate the specified amount of agents, and place them in a valid random manner within the map.
        
        :param agents:  {int}                           Number of agents to be generated.

        :return:        {np.NDArray, list, list}      The map, in the required format as specified in 
                                                        run_experiments.py. The starting position of the agents, given as 
                                                        a list of tuple with integer elements discribing the start 
                                                        locations of the various agents. The end positions provided in the
                                                        exact same structure as the staring postions.
        """
        
        starts_x, starts_y = utils.prime_to_pos(self.rng.choice(self.candidates, agents, replace=False))

        goals_x, goals_y = utils.prime_to_pos(self.rng.choice(self.candidates, agents, replace=False))

        starts = [(starts_y[i], starts_x[i]) for i in range(agents)]
        goals = [(goals_y[i], goals_x[i]) for i in range(agents)]

        return self.map, starts, goals


if __name__ == "__main__":
    test = MapGenerator("maps/assignment_1.map")
    print(test.generate())
