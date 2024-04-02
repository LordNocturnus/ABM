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
        self.agents     = [(0,0), (2,2)]
        self.agent      = 0
        self.radius     = 5
    
    def test_view(self):
        # Test view from agent within box to outside box
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)
        expected = False
        
        self.assertEqual(res[1], expected)

    def test_itself(self):
        # Test view from agent to itself
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)
        expected = False
        
        self.assertEqual(res[0], expected)

    @unittest.expectedFailure
    def test_DEBUG(self):
        # Ensure plot is opened
        # Currently failing because plot is shown and closed at runtime
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles, DEBUG=True)
        
        self.assertTrue(plt.fignum_exists(1))
    

class Test_View_blocking_SC3(unittest.TestCase):
    """
    Test scenario 3
    ----------------
    . . . . .
    . @ @ @ .
    . @ 0 @ .
    . @ @ @ .
    2 . . . 1
    
    Outline of tests:
    ------------------

    test_view : Test to make sure the agent cannot see the in the box but it can see the agent oustide the box  
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.obstacles  = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        self.agents     = [(0,0), (2,2), (2,-2)]
        self.agent      = 1
        self.radius     = 5

    def test_view(self):
        # Test complete view
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)
        expected = [False, False, True]
        
        self.assertListEqual(res, expected)

class Test_View_blocking_SC4(unittest.TestCase):
    """
    Test scenario 4
    ----------------
        0 (x)
        v
    0 > . . 1 . . . .
    (y) . . . . @ . .
        . . . @ . . .
        . . . @ . 0 .
        . . . . . . .
        
    Outline of tests:
    ------------------

    test_view : Generic test to make sure view is as expected from agent 0 
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.obstacles  = [(1, 4), (2, 3), (3, 3)]
        self.agents     = [(3, 5), (0, 2)]
        self.agent      = 0
        self.radius     = 5

    @unittest.expectedFailure
    def test_view(self):
        # Check see trough small gap in walls  (s it can be see, n it cannot see)
        # . n @ s
        # . @ s s
        # . @ s a
        # Currently expected to fail at n -> current algorithm sees n. 
        # Cause is the decreased padding 
        # Solution: currently point of discussion

        # Test complete view
        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)
        expected = [False, False, False, True, True, False]

        self.assertListEqual(res, expected)


class Test_View_blocking_SC5(unittest.TestCase):
    """
    Test scenario 5
    ----------------
        0 (x)
        v
    0 > . . . . . . .
    (y) . . . . 4 @ .
        0 . 1 3 . @ 5
        . . 2 . . @ .
        . . . . . . .
        
    Outline of tests:
    ------------------

    test_increasing_radius : Set of test to make sure view is as expected from agent 0, with constantly
    view radius. To evaluate if view range is implemented correctly.  
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.obstacles  = [(1, 5), (2, 5), (3, 5)]
        self.agents     = [(2, 0), (2, 2), (3, 2), (2, 3), (1, 4), (2, 6)]
        self.agent      = 0

    def test_increasing_radius(self):
        # Test complete view, with chaning view distance (from 0 to 10)
        # Expected output seen below, actual output computed at real time 
        expected = {
            0   : [False, False, False, False, False, False],
            1   : [False, False, False, False, False, False],
            2   : [False, True, False, False, False, False],
            3   : [False, True, True, True, False, False],
            4   : [False, True, True, True, False, False],
            5   : [False, True, True, True, True, False],
            6   : [False, True, True, True, True, False],
            10  : [False, True, True, True, True, False],
        }

        for view_distance, expected_output in expected.items():
            res = view.fov_blocking(self.agent, self.agents, view_distance, self.obstacles)
            with self.subTest():
                self.assertListEqual(expected_output, res, msg=f"Failed at view distance {view_distance}")


@unittest.skip("Test not implemented")
class Test_View_blocking_SC6(unittest.TestCase):
    """
    Test scenario 6
    ----------------
        0 (x)
        v
    0 > . .
    (y) . .
        
    Outline of tests:
    ------------------

    test_visual : Test in which the user will visualy verify if the view map is created as expected. 

    test_conservation_agent : Check if no agents appear or disapear

    test_types : Ensure type consistency
    
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.obstacles  = None
        self.agents     = None
        self.agent      = None
        self.radius     = None

    def test_visual(self):
        view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles, DEBUG=True)

        inp = str(input("\nWas the view as expected? (y/n): ")).strip().lower()

        self.assertIn(inp, ["yes", "y", "1" , "true", "ye"])

    def test_conservation_agents(self):

        # Check if the amount of agents remains constant after return

        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)

        self.assertEqual(len(res), len(self.agents))

    def test_types(self):

        # Check if all returned elements are boolean

        res = view.fov_blocking(self.agent, self.agents, self.radius, self.obstacles)

        self.assertEqual(all(isinstance(el,  bool) for el in res), True)


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
            with self.subTest():
                self.assertIn(expected_output, self.obstacle.segments)

if __name__ == "__main__":
    unittest.main()