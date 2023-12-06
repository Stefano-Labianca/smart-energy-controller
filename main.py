# from appliance.appliances_controller import create_appliances
from time import process_time_ns
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
    Constraint(less_than_five, ["A", "C"]),
    Constraint(greater_than_two, ["A", "B", "C"]),
]

csp_problem = CSP(variables, constraints)

# for v in csp_problem.var_to_const:
#     for c in csp_problem.var_to_const[v]:
#         print(f'{v}: {c}')
#     print('\n')


gnt = GenerateAndTest()
solution = csp_problem.solve(gnt)

