import unittest

from tests.test_integration.test_cbs import Test_Integration_CBS_Disjoint, Test_Integration_CBS_Standard
from tests.test_integration.test_distributed import Test_Integration_Distributed
from tests.test_integration.test_independent import Test_Integration_Independent
from tests.test_integration.test_prioritized import Test_Integration_Prioritized

## Run test instruction
# -- UNITTEST --
# Set directory to parent directory: /ABM
# Run test by running: python -m tests.test_integration.main
# -- PYTEST --
# Set directory to parent directory: /ABM
# Run test by running: pytest tests/test_integration


if __name__ == '__main__':

    print(f"==== Starting full test of all solver models ====")
    
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Integration_Prioritized))
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Integration_CBS_Standard))
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Integration_CBS_Disjoint))
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Integration_Independent))
    test_suite.addTests(test_loader.loadTestsFromTestCase(Test_Integration_Distributed))

    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)