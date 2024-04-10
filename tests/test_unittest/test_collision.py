import unittest

import collisions

class Test_Collision(unittest.TestCase):
    """
    Test the function of the collision detection function used to detect collision within the paths of the agent.
    Its primary use is for the cbs methode, however within the integration tests the function is utelised to
    check if the solution created by the solver is correct and complete -> no collisions. Within the test case 
    a range of cases will be analysed to check the validity of the function.
    """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_sc1(self):
        # There should be a vertex collision detected between agent 0 and 1
        paths = [
            [(0,0)],  # agent 0
            [(0,0)],  # agent 1
        ]
        self.assertTrue(bool(collisions.detect_collisions(paths)))
    
    def test_sc2(self):
        # There should be a vertex collision detected between agent 0 and 1
        paths = [
            [(0,0)],  # agent 0
            [(0,0)],  # agent 1
        ]
        self.assertIn((0,1), collisions.detect_collisions(paths).keys())
    
    def test_sc3(self):
        # There should be only be one collision detected between agent 0 and 1
        paths = [
            [(0,0)],  # agent 0
            [(0,0)],  # agent 1
        ]
        self.assertLessEqual(len(collisions.detect_collisions(paths)), 1)

    def test_sc4(self):
        # There should be no collision found
        paths = [
            [(0,0), (1,0), (2,0), (2,1), (2,2)],  # agent 0
            [(0,1), (0,2), (0,1), (0,0), (1,0)],  # agent 1
        ]
        self.assertFalse(bool(collisions.detect_collisions(paths)))
    
    def test_sc5(self):
        # There should be no collision found
        paths = [
            [(0,0), (1,0), (2,0), (3,0), (4,0)],  # agent 0
            [(1,0), (2,0), (3,0), (4,0), (5,0)],  # agent 1
            [(2,0), (3,0), (4,0), (5,0), (6,0)],  # agent 2
            [(3,0), (4,0), (5,0), (6,0), (7,0)],  # agent 3
        ]
        self.assertFalse(bool(collisions.detect_collisions(paths)))

    def test_sc6(self):
        # Edge collision
        paths = [
            [(0,0), (1,0)],  # agent 0
            [(1,0), (0,0)],  # agent 1
        ]
        self.assertTrue(bool(collisions.detect_collisions(paths)))
    
    def test_sc7(self):
        # Edge collision
        paths = [
            [(0,0), (1,0)],  # agent 0
            [(1,0), (0,0)],  # agent 1
        ]
        self.assertIn("Edge Collision", str(collisions.detect_collisions(paths)[0,1]))
    
    def test_sc8(self):
        # Multiple collsions but only provides first
        paths = [
            [(0,0), (1,0), (2,2)],  # agent 0
            [(1,0), (0,0), (2,2)],  # agent 1
        ]
        self.assertLessEqual(len(collisions.detect_collisions(paths)), 1)

    def test_sc9(self):
        # Multiple collsions: agent 0 and 1 collide and agent 0 and 2 collide
        paths = [
            [(0,0), (1,0), (1,1), (1,2), (2,2)],  # agent 0
            [(0,0), (0,1), (0,2)],  # agent 1
            [(1,1), (1,1), (1,0), (0,0)],  # agent 2
        ]
        self.assertEqual(len(collisions.detect_collisions(paths)), 2)
    
    def test_sc10(self):
        # Multiple collsions: agent 0 and 1 collide and agent 0 and 2 collide
        paths = [
            [(0,0), (1,0), (1,1), (1,2), (2,2)],  # agent 0
            [(0,0), (0,1), (0,2)],  # agent 1
            [(1,1), (1,1), (1,0), (0,0)],  # agent 2
        ]
        self.assertListEqual([(0,1), (0,2)], list(collisions.detect_collisions(paths).keys()))

    def test_sc11(self):
        # Multiple collsions: agent 0 and 1 collide and agent 0 and 2 collide
        paths = [
            [(0,0), (1,0), (1,1), (1,2), (2,2)],  # agent 0
            [(0,0), (0,1), (0,2)],  # agent 1
            [(1,1), (1,1), (1,0), (0,0)],  # agent 2
        ]

        out = list(collisions.detect_collisions(paths).values())
        
        expected = [
            "Vertex collision of agent 0 and agent 1 at timestep 0 at location (0, 0)",
            "Edge Collision of agent 0 and agent 2 at timestep 2 between (1, 0) and (1, 1)"
        ]

        for i in range(len(out)):

            with self.subTest(msg= f"i"):

                self.assertIn(expected[i], str(out[i]))
        

if __name__ == "__main__":
    unittest.main()