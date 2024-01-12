from time import perf_counter_ns

from rich.console import Console
from rich.table import Table

from appliance.appliances_controller import create_variables
from cli.user_cli import UserCLI
from csp_problem.algorithm.dfs import DFS
from csp_problem.algorithm.gac import GAC
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from ontology.appliance_ontology import ApplianceOntology
from utils.pagination import Pagination

console = Console()
# table = Table(title="Performace DFS")
table = Table(title="Performace GAC")


""" Nella documentazione mostrare un grafico finale dove sulle x trovo i test fatti
e sulle y i tempi di ogni test.

Per ogni test ho test 3 barre verticali dove mostrano il tempo di 10, 100 e 1000 iterazioni.
"""


def limit_multimedia(assignment: dict[str, int]) -> bool:
    return all(assignment[v] < 450 for v in assignment)


ontology = ApplianceOntology()
appliances = ontology.create_appliances()

v_names = [
    "computer", "3D_printer", "internet_router", "laptop",
    "phone_charger", "printer", "monitor", "tv", "sound_system",
]


variables = create_variables(appliances, v_names)

constraints = [
    Constraint(limit_multimedia, [
        "computer", "3D_printer", "internet_router", "laptop",
        "phone_charger", "printer", "monitor", "tv", "sound_system"
    ]),
]

csp = CSP(variables, constraints)
dfs = DFS(csp)
gac = GAC(csp)


iterations = [10, 100, 1_000]
times = []

for it_amount in iterations:
    it_times = []

    for _ in range(it_amount):
        start = perf_counter_ns()
        # solutions = dfs.solve()
        solutions = gac.solve()
        end = perf_counter_ns()

        it_times.append(end - start)

    times.append(it_times)


avg_times = []

for time in times:
    avg_time_ns = sum(time) / len(time)
    avg_time_s = (sum(time) / len(time)) / 1e6

    avg_times.append((avg_time_ns, avg_time_s))

table.add_column("Numero di iterazioni", style="blue")
table.add_column("Tempo medio in ns")
table.add_column("Tempo medio in ms")

for i in range(len(iterations)):
    it = iterations[i]
    ns_time, s_time = avg_times[i]

    table.add_row(*(str(it), str(ns_time), str(s_time)))
    table.add_section()


console.print(table)
