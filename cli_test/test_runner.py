from .types import (
    TestAssertionFail,
    TestExceptionFatal,
    ExitCodes
)
from pathlib import Path
from typing import Union, List
from subprocess import run as sub_process_run
from .parsed_output import parsed_output

def run(dir: Union[str, Path]) -> None:

    if not isinstance(dir, Path):
        dir = Path(dir)

    if not dir.exists():
        print('Test directory not found')
        exit(ExitCodes.DIRECTORY_NOT_FOUND)

    tests = Path.glob('**/test_*.py')

    if not tests:
        print('No tests found')
        exit(ExitCodes.NO_TESTS_FOUND)

    errors: List[str] = []
    exit_code = ExitCodes.SUCCESS
    i = 0
    for test in tests:
        try:
            print(f"[{i}] Running test file: {str(test)}")
            output = sub_process_run(['python', str(test)])
            print(parsed_output(output, i))

            i += 1
        except TestExceptionFatal as e:
            errors.append(e)
            print("Fatal exception stopped tests", e)
            exit_code = exit_code | ExitCodes.FATAL_TEST_ERROR
            break
        except TestAssertionFail as exc:
            fails = True
            errors.append(str(exc))
            exit_code = exit_code | ExitCodes.SOME_FAILED
        except Exception as exc:
            fails = True
            errors.append(str(exc))
            exit_code = exit_code | ExitCodes.UNEXPECTED_ERROR
    
        if exit_code & ExitCodes.SOME_FAILED:
            print('Not all tests passed')

        if exit_code & ExitCodes.UNEXPECTED_ERROR:
            print("Some non-test errors occured.")

        exit(exit_code)