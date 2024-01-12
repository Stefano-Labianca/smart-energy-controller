from time import perf_counter_ns

from rich.console import Console
from rich.table import Table

from appliance.appliances_controller import create_appliances, create_variables
from cli.user_cli import UserCLI
from csp_problem.algorithm.dfs import DFS
from csp_problem.algorithm.gac import GAC
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from ontology.appliance_ontology import ApplianceOntology
from utils.pagination import Pagination

""" Nella documentazione mostrare un grafico finale dove sulle x trovo i test fatti
e sulle y i tempi di ogni test.

Per ogni test ho test 3 barre verticali dove mostrano il tempo di 10, 100 e 1000 iterazioni.
"""


def limit_consumption(assignment: dict[str, int]) -> bool:
    return sum(assignment[v] for v in assignment) < 3_000


appliances = create_appliances("./appliance/home.csv")

v_names = [
    "computer",
    "internet_router",
    "phone_charger",
    "monitor",
    "tv",
    "sound_system",
    "freezer",
    "fridge",
    "oven",
    "fryer",
    "vacuum_cleaner"
]


variables = create_variables(appliances, v_names)

constraints = [
    Constraint(limit_consumption, v_names),
]

csp = CSP(variables, constraints)
dfs = DFS(csp)
gac = GAC(csp)


iterations = [1_000]
times = []

console = Console()
# table = Table(title="Performace DFS")
table = Table(title="Performace GAC")


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
