class TestException(Exception):
    ...

class TestExceptionWarning(TestException):
    ...

class TestExceptionFatal(TestException):
    ...

class TestAssertionFail(TestExceptionWarning):
    ...