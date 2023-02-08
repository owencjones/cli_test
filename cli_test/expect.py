from .types import Expectation
from pathlib import Path

def expect(command: str, *args: str) -> Expectation:
    return Expectation(command, args)