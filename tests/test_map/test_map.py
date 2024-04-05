import unittest

import run_experiments
import collisions

from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver

from single_agent_planner_v2 import get_sum_of_cost


class Test_Integration_Map(unittest.TestCase):
    """
    Test class for testing all solvers against one map.
    
    Test Scenarios
    --------------

    Specified map
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_43.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map, starts, goals).find_solution()
        
        # Cost
        print(f"==>Prioritized: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using prioritized for map {my_map}.")

    def test_CBS_Standard(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using CBS-standard <==")

        # Solve 
        my_map, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map, starts, goals).find_solution(False)
        
        # Cost
        print(f"==>CBS-standard: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using CBS-standard for map {my_map}.")
    
    def test_CBS_Disjoint(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using CBS-disjoint <==")

        # Solve 
        my_map, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map, starts, goals).find_solution(True)
        
        # Cost
        print(f"==>CBS-disjoint: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using CBS-disjoint for map {my_map}.")

    def test_Distributed(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using distributed <==")

        # Solve 
        my_map, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")

if __name__ == "__main__":
    unittest.main()