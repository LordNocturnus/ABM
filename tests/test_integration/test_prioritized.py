import unittest
import re
import glob
import os
import pathlib
import sys

import run_experiments
import collisions

from prioritized import PrioritizedPlanningSolver

from single_agent_planner import get_sum_of_cost


class Test_Integration_Prioritized(unittest.TestCase):
    """
    Test class for testing the prioritized solver.
    
    Test Scenarios
    --------------

    Running in all test_*.txt files within the instances directory
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        os.chdir(pathlib.Path(__file__).parent.parent.parent)
        
        # Get all files in the instances folder which are named test
        cls.scenarios = glob.glob("instances/test_*.txt")

        # Sort output https://stackoverflow.com/a/5967539
        def natural_key(str_):
            return [int(el) if el.isdigit() else el for el in re.split(r'(\d+)', str_)]

        cls.scenarios.sort(key= natural_key)

        # Solver mode
        cls.mode = "Prioritized"
    
    def test_tests(self):
        
        for my_map in self.scenarios:

            with self.subTest(msg= f"{my_map} - {self.mode}"):
            
                # Map: my_map
                print(f"==> Solving: {my_map} using {self.mode} <==")

                # Solve 
                my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
                paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing=False).find_solution([])
                
                # Check paths
                collision = bool(collisions.detect_collisions(paths))

                self.assertFalse(collision, msg=f"Failed to find solution using {self.mode} for map {my_map}.")


if __name__ == "__main__":
    unittest.main()
    sys.exit()