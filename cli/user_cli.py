import re
from pickletools import read_uint1

from rich.console import Console
from rich.table import Table

from appliance.Appliance import Appliance
from ontology.appliance_ontology import ApplianceOntology
from utils.pagination import Pagination

console = Console()
ontology = ApplianceOntology()


class UserCLI:
    """Classe di supporto per raccogliere gli input dell'utente
    """

    @classmethod
    def choose_appliances(cls) -> list[dict[str, list[int]]]:
        """Permette di scegliere i dispositivi elettronici da acendere.

        Returns:
            list[dict[str, list[int]]]: Lista di dizionari dove ogni dizionario associa il nome 
            del dispositivo elettronico, ai suoi consumi.
        """

        appliances = ontology.create_appliances()
        cls.create_appliance_table(appliances)

        console.print(
            "\n\nSeleziona i dispositivi elettronici da avviare"
        )

        while True:
            console.print(
                "\n\nSeleziona l'indice di uno o piu' dispositivi, separati da uno spazio (Es. 1 2 6): "
            )

            choosen_appliances = input().strip(" ")

            if cls.is_valid_input(choosen_appliances, appliances):
                objs = cls.take_appliances(choosen_appliances, appliances)

                return cls.take_energy_consumption(objs)

            console.print("Attenzione! Input non corretto.", style="red")

    @classmethod
    def take_appliances(cls, user_input: str, appliances: list[Appliance]) -> list[dict[str, list[int]]]:
        """Prende i dispositivi elettronici scelti dall'utente

        Args:
            user_input (str): Sequenza di indici dell'utente
            appliances (list[Appliance]): Lista di dispotivi elettronici

        Returns:
            list[dict[str, list[int]]]: Lista di dizionari dove ogni dizionario associa il nome 
            del dispositivo elettronico, ai suoi consumi.
        """

        indexs = user_input.split(" ")
        choosen_appliances = []

        for index in indexs:
            a = appliances[int(index) - 1]
            obj = {a._name: a._energy_consumption}

            choosen_appliances.append(obj)

        return choosen_appliances

    @classmethod
    def take_energy_consumption(cls, objs: list[dict[str, list[int]]]) -> list[dict[str, list[int]]]:
        """Prende i consumi elettrici dei dispositivi elettronici scelti dall'utente

        Args:
            objs (list[dict[str, list[int]]]): Contiene tutti i dispositivi presi dall'utente.

        Returns:
            list[dict[str, list[int]]]: Lista di dizionari dove ogni dizionario associa il nome 
            del dispositivo elettronico, ai suoi consumi.
        """

        console.print(
            "\n\nPer ogni tipo di dispositivo elettronico, scegli quale prendere in base al suo consumo\n"
        )

        for i in range(len(objs)):
            obj = objs[i]
            energy = list(obj.values())[0]
            name = list(obj.keys())[0]

            if len(energy) > 1:
                cls.create_energy_consumption_table(name, energy)

                while True:
                    console.print(
                        "Seleziona l'indice di uno o piu' consumi energetici, separati da uno spazio (Es. 1 5): "
                    )

                    choosen_consumption = input().strip(" ")

                    if cls.is_valid_input(choosen_consumption, energy):
                        indexs = choosen_consumption.split(" ")
                        selected_consumption: list[int] = [
                            energy[int(index) - 1] for index in indexs
                        ]

                        obj[name] = selected_consumption
                        objs[i] = obj

                        break

                    console.print(
                        "\nAttenzione! Input non corretto.\n", style="red"
                    )

        return objs

    @classmethod
    def is_valid_input(cls, user_input: str, content: list) -> bool:
        """Verifica se la sequequenza di indici presa in input dall'utente 
        è valida.

        Args:
            user_input (str): Sequenza di indici presa in input dall'utente
            content (list): Lista contenente i dati con cui l'utente deve lavorare

        Returns:
            bool: True se `user_input` è una sequenza valida di indici, altrimenti False.
        """

        if not bool(re.search(r'^(\d+\s)*\d+$', user_input)):
            return False

        indexs = user_input.split(" ")
        max_len = len(content)

        if len(indexs) > max_len:
            return False

        if not all(int(index) - 1 >= 0 and int(index) - 1 <= max_len - 1 for index in indexs):
            return False

        unique_indexs = set(indexs)

        if len(unique_indexs) < len(indexs):
            return False

        return True

    @classmethod
    def create_energy_consumption_table(cls, appliance_name: str, energy: list[int]) -> None:
        """Mostra una tabella da cui prendere i consumi elettronici.

        Args:
            appliance_name (str): Nome del dispositivo elettronico, che sara' il nome della tabella
            energy (list[int]): Consumi energetici.
        """

        table = Table(title=f'{appliance_name}')

        table.add_column("Indice", style="green")
        table.add_column("Consumo energetico")

        for index in range(len(energy)):
            table.add_row(
                str(index + 1), str(energy[index])
            )

            table.add_section()

        console.print(table, "\n")

    @classmethod
    def create_appliance_table(cls, appliances: list[Appliance]) -> None:
        """Mostra tutti i dispositivi elettronici.

        Args:
            appliances (list[Appliance]): Dispositivi elettronici.
        """

        table = Table(title="Elettrodomestici disponibili")

        table.add_column("Indice", style="green")
        table.add_column("Nome")
        table.add_column("Categoria")
        table.add_column("Dimensioni")
        table.add_column("Consumi Energetici")

        for index in range(len(appliances)):
            a = appliances[index]

            table.add_row(
                str(index + 1), a._name, a._category, a._size,
                a._energy_consumption.__str__()
            )
            table.add_section()

        console.print(table)

    @classmethod
    def paginated_partial(cls, pagination: Pagination, names: list[str]) -> None:
        """Mostra in formato tabellare gli assegnamenti parziali che 
        verificano i vincoli del CSP.

        Args:
            pagination (Pagination): Istanza di Pagination
            names (list[str]): Nomi delle variabili presenti nell'assegnamento parziale
        """

        while True:
            pagination.show_partial(names)
            user_input = input("\n> ")

            match user_input:
                case '1': pagination.next_page()
                case '0': pagination.previous_page()
                case _: break

    @classmethod
    def paginated_total(cls, pagination: Pagination) -> None:
        """Mostra in formato tabellare gli assegnamenti totali che 
        verificano i vincoli del CSP.

        Args:
            pagination (Pagination): Istanza di Pagination
        """

        while True:
            pagination.show_total()
            user_input = input("\n> ")

            match user_input:
                case '1': pagination.next_page()
                case '0': pagination.previous_page()
                case _: break
