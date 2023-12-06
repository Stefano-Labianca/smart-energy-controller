# from time import process_time_ns

from appliance.appliances_controller import (create_appliances,
                                             create_variables,
                                             get_variables_name)
from csp_problem.algorithm.generate_and_test import GenerateAndTest
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from csp_problem.Variable import Variable


def limit_consumption(consumption: int) -> bool:
    return consumption < 60_000


appliances = create_appliances()
variables = create_variables(appliances)
variables_name = get_variables_name(variables)

constraints = [
    Constraint(limit_consumption, variables_name),
]

csp_problem = CSP(variables, constraints)

gnt = GenerateAndTest()
solution = csp_problem.solve(gnt)

print(solution)
