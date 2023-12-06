# from appliance.appliances_controller import create_appliances
from csp_problem.algorithm.generate_and_test import GenerateAndTest
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from csp_problem.Variable import Variable


def less_than_five(x: int) -> bool:
    return x < 5


def greater_than_two(x: int) -> bool:
    return x > 2


variables = [
    Variable("A", [1, 4, 3]),
    Variable("B", [4, 9, 2]),
    Variable("C", [6, 10, 3]),
]

constraints = [
    Constraint(less_than_five, ["A", "B", "C"]),
    Constraint(greater_than_two, ["A", "B", "C"]),
]

csp_problem = CSP(variables, constraints)
gnt = GenerateAndTest()

csp_problem.solve(gnt)
