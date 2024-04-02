import unittest

import view


class Test_View_blocking(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    def test_onee(self):
        a = 1
        self.assertEqual(a, 1)

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