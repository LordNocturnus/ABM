import unittest

from types import TracebackType

class CustomTestSummary(unittest.TextTestResult):

    def addSuccess(self, test: unittest.TestCase) -> None:
        super().addSuccess(test)
    
    def addFailure(self, test: unittest.TestCase, err: tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]) -> None:
        super().addFailure(test, err)
    
    def addError(self, test: unittest.TestCase, err: tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]) -> None:
        super().addError(test, err)
    
    def addExpectedFailure(self, test: unittest.TestCase, err: tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]) -> None:
        super().addExpectedFailure(test, err)
    
    def addSubTest(self, test: unittest.TestCase, subtest: unittest.TestCase, err: tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None] | None) -> None:
        super().addSubTest(test, subtest, err)
    
    def addSkip(self, test: unittest.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
    
    def addUnexpectedSuccess(self, test: unittest.TestCase) -> None:
        super().addUnexpectedSuccess(test)