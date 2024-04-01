import unittest

import view

class Test_View_nonblocking(unittest.TestCase):
    """
    Test class to investigate the `fov` function from `view.fov()`

    Outline of tests:
    ------------------

    test_1 upto test_5: Test general functioning of function

    test_6: Test correct implemtation of view radius

    test_7: Test if it can view an agent ontop of itself, but cannot view itself 

    test_conservation_agents: Test if the amount of agents remains constant before 
    and after applying the view function
    
    test_types: Test if the return statement only contains true and false values
    depending on if the mentioned agent can view the other agents.
    
    """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.agent_locations = [(0,0), (1,1), (10,21), (7,2), (3,3), (-1,-4), (-10, -10)]

    
    def test_1(self):

        # Main agent
        self.main_agent = 0
        
        # Define a set view radius
        self.view_distance = 3
        
        # Function output and expected output
        res = view.fov(self.main_agent, self.agent_locations, self.view_distance)
        expected = [False, True, False, False, False, False, False]
        
        # Evaluation
        self.assertEqual(res, expected)
    
    def test_2(self):
        
        # Main agent
        self.main_agent = 0

        # Define a set view radius
        self.view_distance = 0
        
        # Function output and expected output
        res = view.fov(self.main_agent, self.agent_locations, self.view_distance)
        expected = [False, False, False, False, False, False, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_3(self):
        
        # Main agent
        self.main_agent = 0
        
        # Define a set view radius
        self.view_distance = 10
        
        # Function output and expected output
        res = view.fov(self.main_agent, self.agent_locations, self.view_distance)
        expected = [False, True, False, True, True, True, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_4(self):
        
        # Main agent
        self.main_agent = 6
        
        # Define a set view radius
        self.view_distance = 11
        
        # Function output and expected output
        res = view.fov(self.main_agent, self.agent_locations, self.view_distance)
        expected = [False, False, False, False, False, True, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_5(self):
        
        # Main agent
        self.main_agent = 3
        
        # Define a set view radius
        self.view_distance = 100
        
        # Function output and expected output
        res = view.fov(self.main_agent, self.agent_locations, self.view_distance)
        expected = [True, True, True, False, True, True, True]
        
        # Evaluation
        self.assertEqual(res, expected)
    
    def test_6(self):
        
        # Main agent
        self.main_agent = 0

        # Define a set view radius
        self.view_distance = 1
        
        # Function output and expected output
        res = view.fov(self.main_agent, [(0,0), (1,1)], self.view_distance)
        expected = [False, False]
        
        # Evaluation
        self.assertEqual(res, expected)
    
    def test_6(self):
        
        # Main agent
        self.main_agent = 1
        
        # Define a set view radius
        self.view_distance = 1
        
        # Function output and expected output
        res = view.fov(self.main_agent, [(0,0), (0,0)], self.view_distance)
        expected = [True, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_conservation_agents(self):

        # Check if the amount of agents remains constant after return

        self.assertEqual(len(view.fov(0, self.agent_locations, 3)), len(self.agent_locations))

    def test_types(self):

        # Check if all returned elements are boolean

        self.assertEqual(all(isinstance(el,  bool) for el in view.fov(0, self.agent_locations, 3)), True)