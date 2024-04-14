import unittest

import view

class Converter:
    """
    Convert output, to verifiable output. The convert_output function checks if the agents within the map are 
    observable based on the view of the map from an agent. It converts the complex big list structure into a 
    list containing boolean values. Where True indicates the agent can be view and false indicates the agent 
    cannot be viewed. Used to convert test to newer code, besides the additional newer tests added.
    
    """

    covert_output = lambda view_points, agent_locations: [True if agent_loc in view_points else False for agent_loc in agent_locations]


class Test_View_nonblocking(unittest.TestCase):
    """
    Test class to investigate the `fov` function from `view.fov()`

    The output of the view function is precisly known before hand, therfore the
    entire function (that utelises other functions) is tested trough integration tests. 

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
        self.map = None # Map not tested within tis test case

    
    def test_1(self):

        # Main agent
        self.main_agent = self.agent_locations[0]
        
        # Define a set view radius
        self.view_distance = 3
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [False, True, False, False, False, False, False]
        
        # Evaluation
        self.assertEqual(res, expected)
    
    def test_2(self):
        
        # Main agent
        self.main_agent = self.agent_locations[0]

        # Define a set view radius
        self.view_distance = 0
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [False, False, False, False, False, False, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_3(self):
        
        # Main agent
        self.main_agent = self.agent_locations[0]
        
        # Define a set view radius
        self.view_distance = 10
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [False, True, False, True, True, True, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_4(self):
        
        # Main agent
        self.main_agent = self.agent_locations[6]
        
        # Define a set view radius
        self.view_distance = 11
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [False, False, False, False, False, True, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_5(self):
        
        # Main agent
        self.main_agent = self.agent_locations[3]
        
        # Define a set view radius
        self.view_distance = 100
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [True, True, True, False, True, True, True]
        
        # Evaluation
        self.assertEqual(res, expected)
    
    def test_6(self):
        
        # Main agent
        self.main_agent = self.agent_locations[0]

        # Define a set view radius
        self.view_distance = 1
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [False, False, False, False, False, False, False]
        
        # Evaluation
        self.assertEqual(res, expected)
    
    def test_7(self):
        
        # Main agent
        self.main_agent = self.agent_locations[1]
        
        # Define a set view radius
        self.view_distance = 2
        
        # Function output and expected output
        res = Converter.covert_output(view.fov(self.main_agent, self.view_distance, self.map), self.agent_locations)
        expected = [True, False, False, False, False, False, False]
        
        # Evaluation
        self.assertEqual(res, expected)

    def test_conservation_agents(self):

        # Check if the amount of agents remains constant after return
        res = Converter.covert_output(view.fov(self.agent_locations[0], 1, self.map), self.agent_locations)
        self.assertEqual(len(res), len(self.agent_locations))

    def test_types(self):

        # Check if all returned elements are boolean
        res = Converter.covert_output(view.fov(self.agent_locations[0], 1, self.map), self.agent_locations)
        self.assertEqual(all(isinstance(el,  bool) for el in res), True)

if __name__ == "__main__":
    unittest.main()