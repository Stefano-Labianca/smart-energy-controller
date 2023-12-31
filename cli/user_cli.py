from rich.console import Console

from ontology.appliance_ontology import ApplianceOntology

# TODO: Rendere la classe ApplianceOntology un Singleton

console = Console()
ontology = ApplianceOntology()


class UserCLI:

    # TODO: Fase di input da parte dell'utente in cui prende:
    #   1. Uno o più dispositivi
    #   2. Per ogni dispositivo scelto, prende anche il suo consumo
    #   energetico solamente se ne ha più di 1

    @classmethod
    def choose_appliances(cls):
        # appliances = ontology.create_appliances()

        # for a in appliances:
        #     console.print(a)

        return [
            {"computer": [400]}, {"3D_printer": [700]},
            {"oven": [100]},
        ]
