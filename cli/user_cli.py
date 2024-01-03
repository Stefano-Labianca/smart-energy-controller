from rich.console import Console

from ontology.appliance_ontology import ApplianceOntology
from utils.pagination import Pagination

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

    @classmethod
    def paginated_partial(cls, pagination: Pagination, names: list[str]) -> None:
        while True:
            pagination.show_partial(names)
            user_input = input("\n> ")

            match user_input:
                case '1': pagination.next_page()
                case '0': pagination.previous_page()
                case _: break

    @classmethod
    def paginated_total(cls, pagination: Pagination) -> None:
        while True:
            pagination.show_total()
            user_input = input("\n> ")

            match user_input:
                case '1': pagination.next_page()
                case '0': pagination.previous_page()
                case _: break
