from csv import DictReader

from appliance.Appliance import Appliance

MOCK_CSV_PATH = "./appliance/appliances.csv"


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
            name, category, energy_consumption, energy_class, size = row.values()

            appliance = Appliance().name(name).category(
                category).energy_consumption(
                int(energy_consumption)).energy_class(energy_class).size(size)

            appliances.append(appliance)

    return appliances
