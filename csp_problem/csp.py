from csp_problem.Constraint import Constraint
from csp_problem.Variable import Variable


class CSP:
    def __init__(self, variables: list[Variable], constraints: list[Constraint]) -> None:
        self.variables = variables
        self.constraints = constraints
