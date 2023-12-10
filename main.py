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


csp_problem = CSP(variables, constraints)
dfs = DFS(csp_problem)
gac = GAC(csp_problem)

start = time()
solutions = dfs.solve()
solutions = gac.solve()
end = time()

console.log(gac.solve())
console.log(f"Time: {round((end - start) * 1000, 3)}ms", highlight=True)
