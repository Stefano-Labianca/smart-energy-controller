# from appliance.appliances_controller import create_appliances
# from csp_problem.algorithm.generate_and_test import GenerateAndTest
# from csp_problem.csp import CSP

# appliances = create_appliances()

# csp_problem = CSP()
# gnt = GenerateAndTest(domain, 4_000)
# csp_problem.solve()

from csp_problem.Constraint import Constraint
from csp_problem.Variable import Variable


def less_than_five(x: int) -> bool:
    return x < 5


def greater_than_two(x: int) -> bool:
    return x > 2


variable = Variable("computer", [100, 200, 400])

constraints = [
    Constraint(less_than_five),
    Constraint(greater_than_two),
]


for i in range(0, 10):
    print("Numero: ", i, "\tValutazione: ", all(c.evaluate(i)
          for c in constraints))
