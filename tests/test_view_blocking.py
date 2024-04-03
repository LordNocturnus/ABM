import matplotlib.pyplot as plt

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


class Test_View_blocking_SC7(unittest.TestCase):
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
    Test box obstacle object in `view.Box`. Lowest level unittest of the core fundamental elements of the 
    `fov_blocking()` function.

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


class Test_Ray_SC1(unittest.TestCase):
    """
    Test of ray objects, lowest level unittest of the core fundamental elements of the 
    `view.fov_blocking()` function.

    Test scenario 1
    ----------------
        0 (x)
        v
    0 > . s . . .
    (y) . . . . .
        . . . . e

    obstacles placed at run time

    Outline of tests:
    ------------------
    
    test_properties_* : Test correct assignment of coordinates

    test_itersection_* : test intersection algorithm (Expected outcome is intersection)

    test_noitersection_* : test intersection algorithm (Expected outcome is nointersection)

    """
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.start = (0,1)
        self.end = (2,4)
        self.ray = view.Ray(self.start, self.end)

    def test_properties_1(self):
        self.assertEqual(self.start[1], self.ray.start_x)

    def test_properties_2(self):
        self.assertEqual(self.end[0], self.ray.end_y)

    def test_itersection_1(self):
        obstacle = [view.Box((1, 2))]
        self.assertFalse(self.ray.check_view_v2(obstacle))
    
    def test_itersection_2(self):
        obstacle = [view.Box((1, 3))]
        self.assertFalse(self.ray.check_view_v2(obstacle))
    
    def test_itersection_3(self):
        obstacles = [view.Box(el) for el in [(1, 2), (1, 3), (1, 4)]]
        self.assertFalse(self.ray.check_view_v2(obstacles))
        
    def test_nointersection_1(self):
        obstacle = [view.Box((0, 0))]
        self.assertTrue(self.ray.check_view_v2(obstacle))

    def test_nointersection_2(self):
        obstacle = [view.Box((0, 4))]
        self.assertTrue(self.ray.check_view_v2(obstacle))

    def test_nointersection_3(self):
        obstacles = [view.Box(el) for el in [(2, 0), (2, 1), (2, 2)]]
        self.assertTrue(self.ray.check_view_v2(obstacles))


class Test_Ray_SC2(unittest.TestCase):
    """
    Test of ray objects, lowest level unittest of the core fundamental elements of the 
    `view.fov_blocking()` function.

    Test scenario 2
    ----------------
              0 (x)
              v
        . e . . 
        . . . . 
    0 > . . . s 
    (y)

    obstacles placed at run time

    This scenario observes more unique cases in which obstacles are placed differently 
    than in the standard maps. Currently test _2 is expected to fail.

    Outline of tests:
    ------------------

    test_itersection_* : test intersection algorithm (Expected outcome is intersection)
    
    """
    
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        self.start = (0,0)
        self.end = (-2,-2)
        self.ray = view.Ray(self.start, self.end)

    def test_intersection_1(self):
        obstacles = [view.Box(el) for el in [(0, -1), (-1, -1), (-1, 0)]]
        self.assertFalse(self.ray.check_view_v2(obstacles))

    # Failure due to padding, Ray passes trough obstacles with only corners touching
    @unittest.expectedFailure
    def test_intersection_2(self):
        obstacles = [view.Box(el) for el in [(0, -1), (-1, 0)]]
        self.assertFalse(self.ray.check_view_v2(obstacles))


# @unittest.skip("Test not implemented")
class Test_View_coordinates_SC1(unittest.TestCase):
    """
    Test scenario 1: hallway
    ---------------------
    . . . . . .
    . @ @ @ @ .
    . . . 0 . .
    . @ @ @ @ .
    . . . . . .

    Test the view of an agent within a corridor using the `view.agent_vision()` function. The function is part 
    of the `view.fov_blocking()` function. Semi integration/ unittests (medium level)

    Outline of tests:
    ------------------

    test_inview : Test if all points that the agent should view are viewed

    test_wall : Test that the agent cannot see the wall, not that the agent can see the wall, 
    however it should not be able to see anything in it.

    test_notinview : Make sure the agent can't see a range of hand selected points
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.agent = (2, 3)
        self.radius = 3
        # define obstable locations, and load into correct format
        self.obs = [(1, 1), (1, 2), (1, 3), (1, 4), (3, 1), (3, 2), (3, 3), (3, 4)]
        self.obstacles = [view.Box(el) for el in self.obs]

    def test_inview(self):
        # View is complete
        expected = [(2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6)]
        res = view.agent_vision(self.agent, self.radius, self.obstacles)
        self.assertCountEqual(res, expected)
    
    def test_wall(self):
        # Non detection of walls
        res = view.agent_vision(self.agent, self.radius, self.obstacles)
        for id, obstacle in enumerate(self.obs):
            with self.subTest():
                self.assertNotIn(obstacle, res, 
                                 msg=f"Obstacle(id:{id}) placed at {obstacle} was incorrectly labeled as observable, \
                                 by the agent located at {self.agent} with view radius {self.radius}")   

    def test_notinview(self):
        # Checking non occurence of select hand picked values 
        points = [(0,2),(0,3),(0,4),(4,2),(4,3),(4,4)]
        res = view.agent_vision(self.agent, self.radius, self.obstacles)
        for id, point in enumerate(points, start=1):
            with self.subTest():
                self.assertNotIn(point, res, 
                                 msg=f"Point {point} was incorrectly labeled as observable, \
                                 by the agent located at {self.agent} with view radius {self.radius} \
                                 ({id}/{len(points)})")

# @unittest.skip("Test not implemented")
class Test_View_coordinates_SC2(unittest.TestCase):
    """
    Test scenario 2: Exist hallway
    ---------------------
    . . . . . .
    . @ @ @ @ .
    . 0 . . . .
    . @ @ @ @ .
    . . . . . .

    Test the view of an agent leaving a corridor using the `view.agent_vision()` function. 
    The function is part of the `view.fov_blocking()` function. Semi integration/ unittests (medium level)

    Outline of tests:
    ------------------

    test_inview : Test if all points that the agent should view are viewed

    test_wall : Test that the agent cannot see the wall, not that the agent can see the wall, 
    however it should not be able to see anything in it.

    test_notinview : Make sure the agent can't see a range of hand selected points
    """

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.agent = (2, 1)
        self.radius = 2
        # define obstable locations, and load into correct format
        self.obs = [(1, 1), (1, 2), (1, 3), (1, 4), (3, 1), (3, 2), (3, 3), (3, 4)]
        self.obstacles = [view.Box(el) for el in self.obs]

    def test_inview(self):
        # View is complete
        expected = [(2, 2), (2, 3), (1, 0), (2, 0), (3, 0), (2, -1)]
        res = view.agent_vision(self.agent, self.radius, self.obstacles)
        self.assertCountEqual(res, expected)
    
    def test_wall(self):
        # Non detection of walls
        res = view.agent_vision(self.agent, self.radius, self.obstacles)
        for id, obstacle in enumerate(self.obs):
            with self.subTest():
                self.assertNotIn(obstacle, res, 
                                 msg=f"Obstacle(id:{id}) placed at {obstacle} was incorrectly labeled as observable, \
                                 by the agent located at {self.agent} with view radius {self.radius}")   

    def test_notinview(self):
        # Checking non occurence of select hand picked values 
        points = [(1, -1), (3, -1), (2, 4), (0, 2), (4, 2)]
        res = view.agent_vision(self.agent, self.radius, self.obstacles)
        for id, point in enumerate(points, start=1):
            with self.subTest():
                self.assertNotIn(point, res, 
                                 msg=f"Point {point} was incorrectly labeled as observable, \
                                 by the agent located at {self.agent} with view radius {self.radius} \
                                 ({id}/{len(points)})")  

if __name__ == "__main__":
    unittest.main()