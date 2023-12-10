from csv import DictReader

from rich.console import Console

from appliance.Appliance import Appliance
from csp_problem.Variable import Variable

MOCK_CSV_PATH = "./appliance/appliances.csv"
console = Console()


def create_appliances() -> list[Appliance]:
    """Legge da un file csv tutte le informazioni di un elettrodomestico,
    restituendo una lista di istanze della classe Appliance

    Returns:
        list[Appliance]: Lista di istanze di Appliance
    """

    appliances = []

    with open(MOCK_CSV_PATH, newline='') as file:
        iterator = DictReader(file, delimiter=',')

        for row in iterator:
            name, category, energy_consumption,  size = row.values()

            energy_consumption_range = list(
                map(lambda energy: int(energy), energy_consumption.split(", "))
            )

            appliance = Appliance().name(name).category(
                category).energy_consumption(
                    energy_consumption_range).size(size)

            appliances.append(appliance)

    return appliances


def create_variables(appliances: list[Appliance]) -> list[Variable]:
    variables: list[Variable] = []

    for a in appliances:
        variable = Variable(a._name, a._energy_consumption)
        variables.append(variable)

    return variables


def get_variables_name(variables: list[Variable]) -> list[str]:
    variables_name: list[str] = []

    for v in variables:
        variables_name.append(v.name)

    return variables_name


def printer(variables: list[Variable]) -> None:
    for v in variables:
        console.log(v)
