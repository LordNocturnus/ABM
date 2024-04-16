import unittest
import os
import pathlib

import run_experiments
import collisions

from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver

from single_agent_planner_v2 import get_sum_of_cost

os.chdir(pathlib.Path(__file__).parent.parent.parent)


class Test_Integration_Map_1(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_1.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_1.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_1.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_2(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_2.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_2.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_2.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_3(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_3.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_3.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_3.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_4(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_4.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_4.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_4.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_5(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_5.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_5.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_5.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_6(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_6.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_6.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_6.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_7(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_7.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_7.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_7.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_8(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_8.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_8.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_8.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_9(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_9.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_9.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_9.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_10(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_10.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_10.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_10.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_11(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_11.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_11.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_11.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_12(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_12.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_12.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_12.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_13(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_13.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_13.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_13.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_14(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_14.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_14.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_14.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_15(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_15.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_15.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_15.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_16(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_16.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_16.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_16.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_17(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_17.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_17.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_17.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_18(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_18.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_18.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_18.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_19(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_19.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_19.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_19.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_20(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_20.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_20.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_20.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_21(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_21.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_21.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_21.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_22(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_22.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_22.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_22.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_23(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_23.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_23.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_23.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_24(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_24.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_24.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_24.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_25(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_25.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_25.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_25.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_26(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_26.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_26.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_26.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_27(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_27.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_27.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_27.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_28(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_28.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_28.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_28.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_29(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_29.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_29.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_29.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_30(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_30.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_30.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_30.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_31(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_31.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_31.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_31.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_32(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_32.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_32.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_32.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_33(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_33.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_33.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_33.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_34(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_34.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_34.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_34.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_35(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_35.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_35.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_35.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_36(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_36.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_36.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_36.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_37(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_37.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_37.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_37.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_38(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_38.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_38.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_38.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_39(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_39.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_39.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_39.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_40(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_40.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_40.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_40.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_41(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_41.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_41.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_41.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_42(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_42.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_42.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_42.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_43(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_43.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_43.txt
    
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_44(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_44.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_44.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_44.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_45(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_45.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_45.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_45.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_46(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_46.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_46.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_46.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_47(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_47.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_47.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_47.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_48(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_48.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_48.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_48.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_49(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_49.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_49.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_49.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")


class Test_Integration_Map_50(unittest.TestCase):
    """
    Test class for testing all solvers against: instances/test_50.txt. 
    
    Test Scenarios
    --------------

    Specified map: instances/test_50.txt
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    
    @classmethod
    def setUpClass(cls):
        
        # Scenario
        cls.scenario = "instances/test_50.txt"

    def test_Prioritized(self):
            
        # Map: my_map
        my_map = self.scenario
        print(f"==> Solving: {my_map} using prioritized <==")

        # Solve 
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = False).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = CBSSolver(my_map_arr, starts, goals, printing = False, disjoint = True).find_solution([])
        
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
        my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
        paths = DistributedPlanningSolver(my_map_arr, starts, goals).find_solution()
        
        # Cost
        print(f"==>Distributed: cost {get_sum_of_cost(paths)}")

        # Check paths
        collision = bool(collisions.detect_collisions(paths))

        self.assertFalse(collision, msg=f"Failed to find solution using distributed for map {my_map}.")

#### ---- End of tests ---- ####
if __name__ == "__main__":
    unittest.main()