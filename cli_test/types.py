from typing import List, Optional, Any, Union, Callable
from subprocess import run, CompletedProcess, CalledProcessError
from logging import Logger, getLogger
from enum import Enum
from .exceptions import TestAssertionFail, TestExceptionFatal


class Expectation:
    logger: Logger

    command: str
    args: List[str]

    output: Optional[CompletedProcess] = None
    error: Optional[CalledProcessError] = None
    already_run: bool = False

    def __init__(self, command: str, *args: str) -> None:
        self.command = command
        self.args = args

        self.logger = getLogger(__name__)

    def get_whole_string(self) -> str:
        joined_args = " ".join(self.args)
        return f"{self.command} {joined_args}"

    def result_code(self, code: int) -> "Expectation":
        return self.test('returncode', code)

    def std_out(self, stdout: str) -> "Expectation":
        return self.test('stdout', stdout)

    def std_err(self, stderr: str) -> "Expectation":
        return self.test('stderr', stderr)

    def test(self, member: str, expect: Union[Callable[..., bool], Any]) -> "Expectation":
        if not self.already_run:
            return self.execute().test(member, expect)

        if not member in self.output:
            error_message = f"Member {member} was not found in output for command {self.get_whole_string()}"
            self.logger.fatal(error_message)
            raise TestExceptionFatal(error_message)
            
        if isinstance(self.output, CompletedProcess):
            try:
                if isinstance(function, expect):
                    assert expect(self.std_out)
                else:
                    assert expect == self.std_out
                return self
            except AssertionError:
                error_message = f"[{self.get_whole_string()}] expected {str(expect)}, but received {self.output.returncode}"

                self.logger.error(error_message)
                raise TestAssertionFail(error_message)
            except Exception as e:
                self.logger.fatal(f"Unexpected error occurred, for {self.get_whole_string()}", e)
    
    def execute(self) -> "Expectation":
        if self.already_run:
            return self

        try:
            self.output = run([self.command, *self.args])
        except CalledProcessError as exc:
            self.error = exc
        except Exception as exc:
            error_message = f"Execution of command {self.get_whole_string()} failed in unexpected circumstances."
            self.logger.fatal(error_message)
            raise TestExceptionFatal(error_message)
        finally:
            self.already_run = True
            return self