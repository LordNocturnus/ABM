import numpy as np

import unittest

import map_gen


class Test_MapGenerator(unittest.TestCase):
    """
    Test map generator: Map 1 assignment
    ---------------------
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..

    Test to anayse if the map generator function is implemented correctly in `map_gen.MapGenerator()`. 

    Outline of tests:
    ------------------

    test_size : Check expected size of the map

    test_map : Check if the generation of the map is according to the language of the further script

    test_agents_1 : Check amount of agents generated, and if each has a start-goal combination

    test_agents_2 : Check if any start point overlap, or if any goal positions overlapp

    test_agents_3 : 
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.env = map_gen.MapGenerator("maps/assignment_1.map")
        self.nagents = 10
        self.real_map, self.starts, self.goals = self.env.generate(self.nagents)
    
    def test_map(self):
        expected_env = np.array([[0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0]])
        np.testing.assert_array_equal(expected_env, self.real_map)
    
    def test_agents_1(self):
        self.assertTrue(len(self.goals) == len(self.starts) == self.nagents, 
                        msg=f"#goals = {len(self.goals)}, #starts = {len(self.starts)}, #agents = {self.nagents}")
    
    def test_agents_2(self):
        # Check if the amount if the amount of unique goals equals the amount of unique starts equals the amount agents
        self.assertTrue(len(set(self.goals)) == len(set(self.starts)) == self.nagents)


class Test_MapGenerator_RampUp(unittest.TestCase):
    """
    Test map generator: Map 1 assignment
    ---------------------
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..
    ......................
    ..@@@@...@@@@...@@@@..

    Test to anayse if the map generator function is implemented correctly in `map_gen.MapGenerator()`.
    Limit test to ensure the output reemains reliable in limit cases. 

    Outline of tests:
    ------------------

    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.max_count = 20

    def test_size(self):
        for nagents in range(0, self.max_count):
            with self.subTest():
                self.env = map_gen.MapGenerator("maps/assignment_1.map")
                _, starts, goals = self.env.generate(nagents)
                # Check if the amount if the amount of unique goals equals the amount of unique starts equals the amount agents
                self.assertTrue(len(set(goals)) == len(set(starts)) == nagents,
                                msg=f"Failed when loading {nagents} agents. Either double start, or goal found")


if __name__ == "__main__":
    unittest.main()