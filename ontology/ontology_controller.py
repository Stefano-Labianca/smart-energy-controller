import os

from owlready2 import get_ontology, onto_path


class ApplianceOntology:
    def __init__(self) -> None:
        onto_path.append(".")

        self.ontology = get_ontology("./ontology/appliance_ontology.rdf")
        self.ontology.load()

        print(list(self.ontology.classes()))
