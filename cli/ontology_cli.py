import re
from email.mime import application

from rdflib import URIRef
from rich.console import Console

from appliance.Appliance import Appliance
from ontology.appliance_ontology import ApplianceOntology, URIEnum

ontology = ApplianceOntology()
console = Console()

URI_REGEX = '^http?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'
VALID_FIRST_CHAR = '^[a-zA-Z0-9]'
INVALID_CONTENT = '[^a-zA-Z0-9_-]+'


class OntologyCLI:
    """Permette all'utente di interagire con l'ontologia
    """

    """Serve per indicare all'utente quanti nuovi elementi vuole salvare
    all'interno dell'ontologia
    """
    loaded_info: int = 0

    @classmethod
    def show(cls) -> None:
        ontology.show()

    @classmethod
    def add(cls) -> None:
        appliance = cls.__get_appliance()
        ontology.add(appliance)

        cls.loaded_info += 1

    @classmethod
    def remove(cls) -> None:
        individual_uri = cls.__get_uri()

        ontology.remove(individual_uri)

    @classmethod
    def save(cls) -> None:
        if cls.loaded_info > 0:
            ontology.save()

            console.print(
                f"Sono stati salvati {cls.loaded_info} dispositivi.",
                style="green"
            )

            cls.loaded_info = 0

    @classmethod
    def contains(cls) -> None:
        individual_uri = cls.__get_uri()
        found = ontology.contains(individual_uri)

        if found:
            console.print("Individuo trovato!", style="green")
        else:
            console.print("Individuo non trovato", style="yellow")

    @classmethod
    def find(cls) -> None:
        individual_uri = cls.__get_uri()
        triples = ontology.find(individual_uri)

        ontology.show_triples(triples)

    @classmethod
    def __get_uri(cls) -> URIRef:
        while True:
            console.print(
                "\n\nInserire il nome dell'individuo da cercare: "
            )

            name = input().strip(" ")

            if cls.__check_uri(name):
                return URIRef(URIEnum.URI_BASE + name)

            console.print("Nome non valido, riprovare", style="red")

    @classmethod
    def __get_appliance(cls) -> Appliance:
        # TODO: Validazione input
        appliance = Appliance()

        # Perché un'istanza della classe ha questa lista di consumi?
        #   Nel caso si abbiano più dispositivi uguali, tipo 2 computer,
        #   ma con consumi differenti, allora ho scelto di indicare
        #   questi due computer nella stessa istanza, ma che si
        #   differenziano dal consumo.
        # TODO: Va messo nella docs

        while True:
            console.print("Inserire il nome del dispositivo elettronico: ")
            name = input().strip(" ")

            console.print(
                "\nInserire il consumo energetico.\nSe hai piu' dispositivi dello stesso tipo, separa i loro consumi con la virgola: "
            )
            energy = list(
                map(
                    lambda e: int(e),
                    input().strip(" ").split(", ")
                )
            )

            console.print(
                "\nInserire la categoria (Kitchen, Multimedia, Cooling, Washing, Other): "
            )
            category = input().strip(" ")

            console.print(
                "\nInserire le dimensioni (Small, Medium, Large): "
            )
            size = input().strip(" ")

            break

        appliance = appliance.name(name).category(
            category).energy_consumption(energy).size(size)

        return appliance

    @classmethod
    def __check_uri(cls, user_input: str) -> bool:
        if len(user_input) == 0:
            return False

        uri = URIEnum.URI_BASE + user_input

        if not bool(re.search(VALID_FIRST_CHAR, user_input)):
            return False

        if bool(re.search(INVALID_CONTENT, user_input)):
            return False

        if not bool(re.search(URI_REGEX, uri)):
            return False

        return True
