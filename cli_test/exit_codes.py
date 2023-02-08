from enum import Enum


class ExitCodes(Enum):
    SUCCESS = 0
    DIRECTORY_NOT_FOUND = 1
    NO_TESTS_FOUND = 2
    FATAL_TEST_ERROR = 4
    SOME_FAILED = 8
    UNEXPECTED_ERROR = 16