
from rdflib import Graph, Literal
from rdflib.namespace import FOAF, RDF
from rdflib.serializer import Serializer
from rich.console import Console
from rich.table import Table

from appliance.Appliance import Appliance

ONTOLOGY_PATH = "./ontology/appliance_ontology.rdf"
URI_BASE = "http://www.semanticweb.org/utente/ontologies/2023/11/appliances#"
URI_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
OBJECT_INDIVIDUA_TYPE = "http://www.w3.org/2002/07/owl#NamedIndividual"


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
        console = Console()

        table.add_column("Subject", style='blue')
        table.add_column("Predicate", style='blue')
        table.add_column("Object", style='blue')

        for s, p, o in self.g:

            table.add_row(
                *(s.__str__(), p.__str__(), o.__str__()), style="green"
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
        subject = Literal(URI_BASE + individual._name)

        p_energy_consumption = Literal(URI_BASE + 'energy_consumption')
        p_size = Literal(URI_BASE + 'size')
        p_name = Literal(URI_BASE + 'name')

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

        obj_subclass = Literal(URI_BASE + individual._category)

        self.g.add(
            (
                subject, Literal(URI_TYPE), Literal(OBJECT_INDIVIDUA_TYPE)
            )
        )

        self.g.add((subject, Literal(URI_TYPE), obj_subclass))

    def save(self) -> None:
        """Salva permanentemente le modifiche apportate 
        all'ontologia
        """
        self.g.serialize(
            destination=ONTOLOGY_PATH,
            format="pretty-xml"
        )
