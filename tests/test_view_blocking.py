import matplotlib.pyplot as plt

import unittest

import view


class Test_View_blocking_SC2(unittest.TestCase):
    """
    Test scenario 2
    ----------------
    . . . . 1
    . @ @ @ .
    . @ 0 @ .
    . @ @ @ .
    . . . . .
    
    Outline of tests:
    ------------------

    test_view : Test to make sure the agent inside the box cannot see the other agent outised the box

    test_itself : Test to make sure agent cannot see itself

    test_DEBUG (currently expected to fail) : Check if the debig window is opened  
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.obstacles  = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        self.agents     = [(0,0), (1,1)]
        self.agent      = 0
        self.radius     = 5
    
    def test_view(self):
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)
        expected = False
        self.assertEqual(res[1], expected)

    def test_itself(self):
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)
        expected = False
        self.assertEqual(res[0], expected)

    @unittest.expectedFailure
    def test_DEBUG(self):
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles, DEBUG=True)
        self.assertTrue(plt.fignum_exists(1))
    


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