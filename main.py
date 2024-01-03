from appliance.Appliance import Appliance
from appliance.appliances_controller import create_variables
from cli.user_cli import UserCLI
from csp_problem.algorithm.dfs import DFS
from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from knowledge_base.expert_system import run_expert_system
from ontology.appliance_ontology import ApplianceOntology
from utils.pagination import Pagination


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


ontology = ApplianceOntology()
appliances = ontology.create_appliances()

variables = create_variables(appliances)
constraints = [
    Constraint(limit_multimedia, [
        "computer", "3D_printer", "internet_router", "laptop",
        "phone_charger", "printer", "monitor", "tv", "sound_system"
    ]),
    Constraint(limit_cooling, [
        "air_conditioner", "fan", "air_purifier"
    ]),
]

csp = CSP(variables, constraints)
dfs = DFS(csp)
solutions = dfs.solve()

names = [
    "computer", "3D_printer", "internet_router", "laptop",
    "phone_charger", "printer", "monitor", "tv", "sound_system",
    "air_conditioner", "fan", "air_purifier"
]

run_expert_system(1.5)
pagination = Pagination(solutions)


UserCLI.paginated_partial(pagination, names)
UserCLI.paginated_total(pagination)
