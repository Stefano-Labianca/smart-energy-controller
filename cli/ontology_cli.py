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
    """Permette all'utente di interagire con l'ontologia.
    """

    """Serve per indicare all'utente quanti, nuovi elementi, vuole salvare
    all'interno dell'ontologia.
    """
    loaded_info: int = 0

    @classmethod
    def show(cls) -> None:
        """L'utente ha scelto di visualizzare le 
        informazioni dell'ontologia
        """
        ontology.show()

    @classmethod
    def add(cls) -> None:
        """L'utente ha scelto di aggiungere 
        un individuo all'ontologia
        """
        appliance = cls.__get_appliance()
        ontology.add(appliance)

        cls.loaded_info += 1

    @classmethod
    def remove(cls) -> None:
        """L'utente ha scelto di rimuovere 
        un individuo dall'ontologia
        """
        individual_uri = cls.__get_uri()
        ontology.remove(individual_uri)

    @classmethod
    def save(cls) -> None:
        """L'utente vuole salvare le modifiche applicate 
        all'ontologia permanentemente
        """
        if cls.loaded_info > 0:
            ontology.save()

            console.print(
                f"Sono stati salvati {cls.loaded_info} dispositivi.",
                style="green"
            )

            cls.loaded_info = 0

    @classmethod
    def contains(cls) -> None:
        """L'utente vuole sapere se un individuo è 
        presente nell'ontologia
        """
        individual_uri = cls.__get_uri()
        found = ontology.contains(individual_uri)

        if found:
            console.print("Individuo trovato!", style="green")
        else:
            console.print("Individuo non trovato", style="yellow")

    @classmethod
    def find(cls) -> None:
        """L'utente vuole trovare un individuo 
        nell'ontologia
        """
        individual_uri = cls.__get_uri()
        triples = ontology.find(individual_uri)

        ontology.show_triples(triples)

    @classmethod
    def __get_uri(cls) -> URIRef:
        """Permette all'utente di creare l'URI di un individuo
        partendo dal suo nome, preso in input.

        Returns:
            URIRef: URI dell'individuo.
        """
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
        """Permette la raccolta delle informazioni di un dispositivo
        elettronico, da parte dell'utente, che vengono restituite come
        istanza della classe Appliance.

        Returns:
            Appliance: Dispositivo elettronico dell'utente.
        """

        appliance = Appliance()
        name = ""
        energy = []
        category = ""
        size = ""

        # Perché un'istanza della classe ha questa lista di consumi?
        #   Nel caso si abbiano più dispositivi uguali, tipo 2 computer,
        #   ma con consumi differenti, allora ho scelto di indicare
        #   questi due computer nella stessa istanza, ma che si
        #   differenziano dal consumo.
        # TODO: Va messo nella docs

        while True:
            console.print(
                "Inserire il nome del dispositivo elettronico: ",
                style="blue"
            )
            name = input().strip(" ")

            if cls.__check_name(name):
                break

            console.print("Nome non valido.", style="red")

        while True:
            console.print(
                "\nInserire il consumo energetico.\nSe hai piu' dispositivi dello stesso tipo, separa i loro consumi con uno spazio: ",
                style="blue"
            )
            energy_input = input().strip(" ")
            energy_input = re.sub(r'\s+', " ", energy_input)

            if cls.__check_energy_consumption(energy_input):
                energy = list(
                    map(
                        lambda e: int(e),
                        energy_input.split(" ")
                    )
                )

                break

            console.print("Valori non validi.", style="red")

        while True:
            console.print(
                "\nInserire la categoria (Kitchen, Multimedia, Cooling, Washing, Other): ",
                style="blue"
            )
            category = input().strip(" ")

            if cls.__check_category(category):
                category = category.lower().capitalize()
                break

            console.print("Categoria non valida.", style="red")

        while True:
            console.print(
                "\nInserire le dimensioni (small, medium, large): ",
                style="blue"
            )
            size = input().strip(" ")

            if cls.__check_size(size):
                size = size.lower()
                break

            console.print("Dimensioni non valide.", style="red")

        appliance = appliance.name(name).category(
            category).energy_consumption(energy).size(size)

        return appliance

    @classmethod
    def __check_uri(cls, user_input: str) -> bool:
        """Verifica la correttezza dell'URI di un individuo, andando
        a controllare prima se il nome fornito è valido.

        Args:
            user_input (str): Nome dell'individuo

        Returns:
            bool: True se ho un URI valido, altrimenti False.
        """
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

    @classmethod
    def __check_name(cls, user_input: str) -> bool:
        if len(user_input) == 0:
            return False

        if not bool(re.search(VALID_FIRST_CHAR, user_input)):
            return False

        if bool(re.search(INVALID_CONTENT, user_input)):
            return False

        return True

    @classmethod
    def __check_energy_consumption(cls, user_input: str) -> bool:
        if len(user_input) == 0:
            return False

        if not bool(re.search(r'^(\d+\s)*\d+$', user_input)):
            return False

        return True

    @classmethod
    def __check_category(cls, user_input: str) -> bool:
        if len(user_input) == 0:
            return False

        user_input = user_input.lower().capitalize()

        match user_input:
            case 'Multimedia': return True
            case 'Kitchen': return True
            case 'Washing': return True
            case 'Cooling': return True
            case 'Other': return True
            case _: return False

    @classmethod
    def __check_size(cls, user_input: str) -> bool:
        if len(user_input) == 0:
            return False

        user_input = user_input.lower()

        match user_input:
            case 'small': return True
            case 'medium': return True
            case 'large': return True
            case _: return False
