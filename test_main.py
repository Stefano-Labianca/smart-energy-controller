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

# Definizione dei vincoli
# Un vincolo deve accettare un assegnamento di tipo `dict[str, int]`
# e deve restituire un booleano


def limit_multimedia(assignment: dict[str, int]) -> bool:
    return all(assignment[v] < 1 for v in assignment)


console = Console()
table = Table(title="Provola")

ontology = ApplianceOntology()
appliances = ontology.create_appliances()

# Contiene tutti i nomi delle variabili che consideri
v_names = [
    "computer", "3D_printer", "internet_router", "laptop",
    "phone_charger", "printer", "monitor", "tv", "sound_system",
]

# Inizializza le variabili e i vincoli
variables = create_variables(appliances, v_names)
constraints = [
    Constraint(limit_multimedia, v_names),
]

# Inizializzo i problema
csp = CSP(variables, constraints)
dfs = DFS(csp)
gac = GAC(csp)


solutions = dfs.solve()
# solutions = gac.solve()

# Faccio visualizzare i risultati
pagination = Pagination(solutions)
UserCLI.paginated_total(pagination)
