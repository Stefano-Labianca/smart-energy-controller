from csv import DictReader

from appliance.Appliance import Appliance
from csp_problem.Variable import Variable

MOCK_CSV_PATH = "./appliance/appliances.csv"


def create_appliances(csv_path=MOCK_CSV_PATH) -> list[Appliance]:
    """Legge da un file csv tutte le informazioni di un elettrodomestico,
    restituendo una lista di istanze della classe Appliance

    Returns:
        list[Appliance]: Lista di istanze di Appliance
    """

    appliances = []

    with open(csv_path, newline='') as file:
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


def create_variables(appliances: list[Appliance], v_names: list[str]) -> list[Variable]:
    variables: list[Variable] = [
        Variable(a._name, a._energy_consumption)
        for a in appliances
        if a._name in v_names
    ]

    return variables


def get_variables_name(variables: list[Variable]) -> list[str]:
    variables_name: list[str] = []

    for v in variables:
        variables_name.append(v.name)

    return variables_name
