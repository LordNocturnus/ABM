import unittest

import view


class Test_View_blocking(unittest.TestCase):

    def test_onee(self):
        a = 1
        self.assertEqual(a, 1)