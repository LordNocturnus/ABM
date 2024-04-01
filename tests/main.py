import unittest

from tests import test_view_nonblocking
from tests import test_view_blocking
from tests import test_mapgen
from tests import summary

## Run test instruction
# Set directory to parent directory: /ABM
# Run test by running python -m tests.main

if __name__ == '__main__':
    
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(test_loader.loadTestsFromTestCase(test_view_nonblocking.Test_View_nonblocking))
    test_suite.addTests(test_loader.loadTestsFromTestCase(test_view_blocking.Test_View_blocking))
    test_suite.addTests(test_loader.loadTestsFromTestCase(test_mapgen.Test_MapGenerator))
    
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)