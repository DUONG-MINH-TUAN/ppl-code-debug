from abc import ABC, abstractmethod
from typing import List, Optional

# from interpreter.context import Context


class Expression:
    def __init__(self, line: int):
        self.line = line

    def interpret(self, context):
        pass