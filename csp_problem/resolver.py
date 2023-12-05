from abc import ABC, abstractmethod

from csp_problem.Constraint import Constraint
from csp_problem.Variable import Variable


class Resolver(ABC):

    @abstractmethod
    def solve(self, variables: list[Variable], constraints: list[Constraint]) -> list:
        raise NotImplementedError
