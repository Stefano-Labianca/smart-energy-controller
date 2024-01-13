
from rich.console import Console

from appliance.appliances_controller import (create_appliances,
                                             create_variables,
                                             get_variables_name)
from csp_problem.algorithm.dfs import DFS
from csp_problem.algorithm.gac import GAC
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from utils.printer import assignments_printer


def limit_multimedia(assignment: dict[str, int]) -> bool:
    accumulator = 0

    for v in assignment:
        accumulator = accumulator + (assignment[v] * 24)
    return accumulator < 35_000


def limit_cooling(assignment: dict[str, int]) -> bool:
    accumulator = 0

    for v in assignment:
        accumulator = accumulator + (assignment[v] * 24)
    return accumulator < 15_000


console = Console()

names = [
    "computer", "3D_printer", "internet_router", "laptop",
    "phone_charger", "printer", "monitor", "tv", "sound_system",
    "air_conditioner", "fan", "air_purifier"
]

appliances = create_appliances()
variables = create_variables(appliances, names)
variables_name = get_variables_name(variables)


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

solutions = []

# solutions = dfs.solve()
solutions = gac.solve()

assignments_printer(solutions)