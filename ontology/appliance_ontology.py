
import re
from enum import StrEnum
from unicodedata import category

from rdflib import Graph, Literal, URIRef
from rich.console import Console
from rich.table import Table

from appliance.Appliance import Appliance

ONTOLOGY_PATH = "./ontology/appliance_ontology.rdf"


class URIEnum(StrEnum):
    URI_BASE = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#"
    URI_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    OBJECT_INDIVIDUA_TYPE = "http://www.w3.org/2002/07/owl#NamedIndividual"
    OWL_CLASS = "http://www.w3.org/2002/07/owl#Class"
    OWL_THING = "http://www.w3.org/2002/07/owl#Thing"
    BASE_CLASS_URI = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#Appliance"
    DATA_TYPE_URI = "http://www.w3.org/2002/07/owl#DatatypeProperty"
    TOP_DATA_PROPERTY = "http://www.w3.org/2002/07/owl#topDataProperty"
    STRING_SCHEMA_URI = "http://www.w3.org/2001/XMLSchema#string"


class CategoryEnum(StrEnum):
    OTHER = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#Other"
    MULTIMEDIA = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#Multimedia"
    WASHING = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#Washing"
    COOLING = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#Cooling"
    KITCHEN = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#Kitchen"


class SizeEnum(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


console = Console()


class ApplianceOntology:
    """Permette la lavorazione delle ontologie
    """

    def __init__(self) -> None:
        self.g = Graph()
        self.g.parse(ONTOLOGY_PATH)

    def show(self) -> None:
        """Mostra le informazioni dell'ontologia, 
        nella forma (Soggetto, Predicato, Oggetto).
        """

        table = Table(title="Triples")

        table.add_column("Subject", style='blue')
        table.add_column("Predicate", style='blue')
        table.add_column("Object", style='blue')

        for s, p, o in self.g:
            table.add_row(
                *(s.__str__(), p.__str__(), o.__str__()), style="green"
            )
            table.add_section()

        console.print(table)

    def show_triple(self, tiple) -> None:
        table = Table(title="Triple")

        table.add_column("Subject", style='blue')
        table.add_column("Predicate", style='blue')
        table.add_column("Object", style='blue')

        table.add_row(
            tiple[0].__str__(),
            tiple[1].__str__(),
            tiple[2].__str__(),
        )

        console.print(table)

    def show_triples(self, triples: list) -> None:
        table = Table(title="Triples")

        table.add_column("Subject", style='blue')
        table.add_column("Predicate", style='blue')
        table.add_column("Object", style='blue')

        for t in triples:
            table.add_row(
                t[0].__str__(),
                t[1].__str__(),
                t[2].__str__(),
            )

            table.add_section()

        console.print(table)

    def add(self, individual: Appliance) -> None:
        """Aggiunge un nuovo individuo all'interno dell'ontologia.
        Per salvare in maniera consistente gli aggiornamenti fatti, è 
        necessario richiamare il metodo `save`.

        Args:
            individual (Appliance): Individuo da aggiungere
        """
        subject = URIRef(URIEnum.URI_BASE + individual._name)

        p_energy_consumption = Literal(URIEnum.URI_BASE + 'energy_consumption')
        p_size = Literal(URIEnum.URI_BASE + 'size')
        p_name = Literal(URIEnum.URI_BASE + 'name')

        energy_consumption_list = list(
            map(
                lambda e: str(e),
                individual._energy_consumption
            )
        )

        obj_energy_consumption = Literal(
            ", ".join(energy_consumption_list)
        )
        obj_size = Literal(individual._size)
        obj_name = Literal(individual._name)

        self.g.add((subject, p_energy_consumption, obj_energy_consumption))
        self.g.add((subject, p_size, obj_size))
        self.g.add((subject, p_name, obj_name))

        obj_subclass = Literal(URIEnum.URI_BASE + individual._category)

        self.g.add(
            (
                subject,
                Literal(URIEnum.URI_TYPE),
                Literal(URIEnum.OBJECT_INDIVIDUA_TYPE)
            )
        )

        self.g.add((subject, Literal(URIEnum.URI_TYPE), obj_subclass))

    def remove(self, uri: URIRef) -> None:
        """Rimuove un individuo dall'ontologia.
        Per salvare in maniera consistente gli aggiornamenti fatti, è 
        necessario richiamare il metodo `save`.

        Args:
            uri (URIRef): Identificativo dell'individuo
        """
        self.g.remove((uri, None, None))

    def save(self) -> None:
        """Salva permanentemente le modifiche apportate 
        all'ontologia
        """
        self.g.serialize(
            destination=ONTOLOGY_PATH,
            format="pretty-xml"
        )

    def contains(self, uri: URIRef) -> bool:
        """Verifica se l'identificatore di un individuo è presente 
        nel grafo, restituendo True in caso affermativo, False in caso
        contrario

        Args:
            uri (URIRef): Identificativo dell'individuo

        Returns:
            bool: Esito della ricerca
        """
        return (uri, None, None) in self.g

    def find(self, uri: URIRef) -> list[tuple]:
        """Restituisce una lista contenente tutte quelle tuple 
        che corrispondono all'uri fornito.

        Args:
            uri (URIRef): Identificatore dell'individuo

        Returns:
            list[tuple]: Lista di tuple che contengono come soggetto l'uri dato
        """
        return list(self.g.triples((uri, None, None)))

    def create_appliance(self) -> list[Appliance]:
        """Restituisce una lista di instanze di Appliance, che rappresenteranno
        gli elettrodomestici contenuti nell'ontologia

        Returns:
            list[Appliance]: Lista di elettrodomestici
        """
        sub_obj = list(self.g.subject_objects())
        only_base_uri = [
            pair for pair in sub_obj if URIEnum.URI_BASE in pair[0].__str__()
        ]

        filtered_data = self.__filter_data(only_base_uri)

        return self.__build_appliances(filtered_data)

    def __build_appliances(self, pairs: list[tuple]) -> list[Appliance]:
        """Permette di costruire la lista di elettrodomestici

        Args:
            pairs (list[tuple]): Informazioni prese dall'ontologia sottoforma di coppie
            (soggetto, oggetto).

        Returns:
            list[Appliance]: Lista di istanze di Appliance
        """

        appliances: list[Appliance] = []

        while len(pairs) > 0:
            appliace = Appliance()
            pair = pairs[0]

            uri: str = pair[0].__str__()
            info = self.__get_appliance_info(uri, pairs)

            for field in info:
                field_data = field[1].__str__()

                if self.__is_category_field(field_data):
                    category = field_data.split("#")[1]
                    appliace = appliace.category(category)

                elif self.__is_size_field(field_data):
                    appliace = appliace.size(field_data)

                elif self.__is_energy_consumption_field(field_data):
                    w = field_data.split(", ")
                    energy_consumption = list(
                        map(lambda x: int(x), w)
                    )

                    appliace = appliace.energy_consumption(energy_consumption)

                else:
                    appliace = appliace.name(field_data)

            pairs = [pair for pair in pairs if uri != pair[0].__str__()]
            appliances.append(appliace)

        return appliances

    def __filter_data(self, pairs: list[tuple]) -> list[tuple]:
        """Permette la rimozione di tutti quei campi che non rappresentano
        istanze di Appliance.

        Args:
            pairs (list[tuple]): Informazioni prese dall'ontologia sottoforma di coppie
            (soggetto, oggetto)

        Returns:
            list[tuple]: coppie (soggetto, oggetto) filtrate con le informazioni necessarie per crecare
            delle istanze di Appliance
        """

        removed_individual_type = self.__remove_uri(
            URIEnum.OBJECT_INDIVIDUA_TYPE,
            pairs
        )

        removed_class = self.__remove_uri(
            URIEnum.OWL_CLASS, removed_individual_type
        )

        removed_thing = self.__remove_uri(
            URIEnum.OWL_THING, removed_class
        )

        removed_base_class = self.__remove_uri(
            URIEnum.BASE_CLASS_URI, removed_thing
        )

        removed_data_types = self.__remove_uri(
            URIEnum.DATA_TYPE_URI, removed_base_class
        )

        removed_top_data_property = self.__remove_uri(
            URIEnum.TOP_DATA_PROPERTY, removed_data_types
        )

        removed_string_schema = self.__remove_uri(
            URIEnum.STRING_SCHEMA_URI, removed_top_data_property
        )

        return removed_string_schema

    def __remove_uri(self, uri: str, pairs: list[tuple]) -> list[tuple]:
        return [pair for pair in pairs if uri not in pair[1].__str__()]

    def __is_category_field(self, field: str):
        return field in CategoryEnum

    def __is_size_field(self, field: str):
        return field in SizeEnum

    def __is_energy_consumption_field(self, field: str):
        return bool(re.search(r'^(\d+,\s)*\d+$', field))

    def __get_appliance_info(self, uri: str, pairs: list[tuple]):
        return [
            pair for pair in pairs if uri in pair[0].__str__()
        ]
