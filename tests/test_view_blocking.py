import unittest

import view


class Test_View_blocking_SC1(unittest.TestCase):
    """
    Test scenario 1: Wall
    ---------------------
    1 . 2 3 .
    . @ @ @ 4
    . . 0 . .
    5 . . . .

    Outline of tests (name function/test + short description):
    ---------------------
    test_11 and test_12 both test whether the agent 0 is able to see what we expect them to see with different radii
    test_21 and test_22 both test the sight of an agent close to another agent and whether it can see through them

    """

    #Scenario wall
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        #define agent locations
        self.agent_locations = [(2, 2), (0, 0), (0, 2), (0, 3), (1, 4), (3, 0)]
        #define obstable locations
        self.obstacles = [(1, 1), (1, 2), (1, 3)]

    def test_11(self):
        #agent
        self.main_agent = 0

        #view
        self.view_distance = 2

        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, False, False, False, False, False]

        #evaluation
        self.assertEqual(res, expected)

    def test_12(self):
        # agent
        self.main_agent = 0

        # view
        self.view_distance = 3

        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, False, False, False, False, True]

        # evaluation
        self.assertEqual(res, expected)

    def test_21(self):
        # agent
        self.main_agent = 3

        # view
        self.view_distance = 2

        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, False, True, False, True, False]

        # evaluation
        self.assertEqual(res, expected)

    def test_22(self):
        # agent
        self.main_agent = 3

        # view
        self.view_distance = 3

        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, True, True, False, True, False]

        # evaluation
        self.assertEqual(res, expected)


class Test_View_blocking_SC3(unittest.TestCase):
    """
        Test scenario 1: hallway
        ---------------------
        . 3 . . . .
        . @ @ @ @ 4
        0 . . 1 2 .
        . @ @ @ @ .
        . . 5 6 . 7

        Outline of tests (name function/test + short description):
        ---------------------
        test_11 and test_21 test whether the agent can propertly 'see' through the hallway at different radii
        test_21 and test_22 test the same as test_1 but different agent with more agents in view

        """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        # define agent locations
        self.agent_locations = [(2, 0), (2, 3), (2, 4), (0, 1), (1, 5), (4, 2), (4, 3), (4, 5)]
        # define obstable locations
        self.obstacles = [(1, 1), (1, 2), (1, 3), (1, 4), (3, 1), (3, 2), (3, 3), (3, 4)]

    def test_11(self):
        self.main_agent = 0
        self.view_distance = 3
        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, True, False, False, False, False, False, False]

        self.assertEqual(res, expected)

    def test_12(self):
        self.main_agent = 0
        self.view_distance = 5
        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, True, True, False, False, False, False, False]

        self.assertEqual(res, expected)

    def test_21(self):
        self.main_agent = 2
        self.view_distance = 3
        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [False, True, False, False, True, False, False, False]

        self.assertEqual(res, expected)

    def test_22(self):
        self.main_agent = 2
        self.view_distance = 5
        res = view.fov_blocking(self.main_agent, self.agent_locations, self.view_distance, self.obstacles)
        expected = [True, True, False, False, True, False, False, False]

        self.assertEqual(res, expected)

class Test_Obstacle(unittest.TestCase):
    """
    Test box obstacle object in `view.Box`

    Outline of tests:
    ------------------

    test_objectproperties_1: Test if the right positions are assigned to the box

    test_objectproperties_2: This if the right outer bounds are assigned, for collision detection

    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        # Initialise obstacle location for testing
        self.location = (5,4)
    
    @classmethod
    def setUpClass(cls):
        # Initialise obstacle object
        cls.obstacle = view.Box((5,4))

    def test_objectproperties_1(self):
        # Test if the right properties of the box are stored within the onbject
        self.assertDictContainsSubset({"x":4, "y":5}, self.obstacle.__dict__,
                                      msg="Obstecle object created in incorrect manner")

    def test_objectproperties_2(self):
        # Test if the right properties of the box are stored within the onbject
        expected = [[(5.49, 4.49), (4.51, 4.49)], [(5.49, 4.49), (5.49, 3.51)],
                    [(4.51, 3.51), (4.51, 4.49)], [(4.51, 3.51), (5.49, 3.51)]]
        
        for expected_output in expected:
            with self.subTest(input=self.obstacle.segments, expected=expected_output):
                self.assertIn(expected_output, self.obstacle.segments)

if __name__ == "__main__":
    unittest.main()