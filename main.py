from time import time

from rich.console import Console

from appliance.appliances_controller import (create_appliances,
                                             create_variables,
                                             get_variables_name, printer)
from csp_problem.algorithm.dfs import DFS
from csp_problem.algorithm.gac import GAC
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from csp_problem.Variable import Variable

# from rich.table import Table


def limit_multimedia(assignment: dict[Variable, int]) -> bool:
    accumulator = 0

    for v in assignment:
        accumulator = accumulator + (assignment[v] * 24)
    return accumulator < 35_000


def limit_cooling(assignment: dict[Variable, int]) -> bool:
    accumulator = 0

    for v in assignment:
        accumulator = accumulator + (assignment[v] * 24)
    return accumulator < 15_000


# table = Table(title="Info", highlight=True)
console = Console()


appliances = create_appliances()
variables = create_variables(appliances)
variables_name = get_variables_name(variables)


# columns = [
#     "computer", "3D_printer", "internet_router", "laptop",
#     "phone_charger", "printer", "monitor", "tv", "sound_system",
#     "air_conditioner", "fan", "air_purifier"
# ]


# for c in columns:
#     table.add_column(c)

constraints = [
    Constraint(limit_multimedia, [
        "computer", "3D_printer", "internet_router", "laptop",
        "phone_charger", "printer", "monitor", "tv", "sound_system"
    ]),
    Constraint(limit_cooling, [
        "air_conditioner", "fan", "air_purifier"
    ]),
]

""" TEST CSP

def a_lt_b(assignment: dict[str, int]):
    a = assignment['A']
    b = assignment['B']

    return a < b


def b_lt_c(assignment: dict[str, int]):
    b = assignment['B']
    c = assignment['C']

    return b < c


variables = [
    Variable('A', [1, 2, 3, 4]),
    Variable('B', [1, 2, 3, 4]),
    Variable('C', [1, 2, 3, 4]),
]

constraints = [
    Constraint(a_lt_b, ['A', 'B']),
    Constraint(b_lt_c, ['B', 'C']),
]"""


# # printer(variables)

# for v in variables:
#     new_domain = new_domains.get(v.name)

#     if new_domain:
#         v.update_domain(new_domain)

# console.log("------------------------")

# printer(variables)


csp_problem = CSP(variables, constraints)
# dfs = DFS()
gac = GAC(variables, constraints)
solutions = gac.solve()

console.log(solutions)
# Uso del DFS
# start = time()
# solutions = csp_problem.solve(dfs)
# end = time()

# print("Time: ", end - start, "s")
