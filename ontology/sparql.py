from enum import StrEnum
from typing import Self

from owlready2 import Ontology, default_world, get_ontology, onto_path

from utils.printer import query_result_printer

ONTOLOGY_PATH = "./ontology/appliance_ontology.rdf"


class OWLType(StrEnum):
    DATA_TYPE_PROPERTY = "owl:DatatypeProperty"
    CLASS = "owl:Class"
    NAMED_INDIVIDUAL = "owl:NamedIndividual"


class SPARQL:
    """Wrapper per attuare delle query all'interno 
    di un ontologia
    """

    def __init__(self) -> None:
        self.query: str = ""
        self.variables = ""

    def select(self, what: list[str] = []) -> Self:
        if len(what) == 0:
            self.query = "SELECT *"

        else:
            variables: str = ""

            for v in what:
                variables += '?' + v + ' '

            self.query = "SELECT " + variables

        self.variables = list(what)

        return self

    def where(self, conditions: list[str]) -> Self:
        where_clause: str = "WHERE {"

        if len(self.variables) > 1:
            for i in range(len(conditions)):
                where_clause += ' ?' + \
                    self.variables[i] + ' a ' + conditions[i] + ' . '
        else:
            where_clause += ' ?x' + ' a ' + conditions[0] + ' . '

        where_clause += "}"

        self.query += where_clause

        return self

    def execute(self) -> None:
        result = default_world.sparql(self.query)

        if len(self.variables) == 0:
            query_result_printer(list(result), ['x'])  # type: ignore
        else:
            query_result_printer(list(result), self.variables)  # type: ignore
