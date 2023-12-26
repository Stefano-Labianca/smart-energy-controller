import os
from typing import Literal

from owlready2 import Ontology, ThingClass, get_ontology, onto_path
from owlready2.individual import NamedIndividual

from appliance.Appliance import Appliance

type ClassName = Literal[
    "Appliance", "Washing", "Kitchen",
    "Other", "Multimedia", "Cooling"
]

ONTOLOGY_PATH = "./ontology/appliance_ontology.rdf"


class ApplianceOntology:
    def __init__(self) -> None:
        onto_path.append(".")

        self.ontology: Ontology = get_ontology(
            ONTOLOGY_PATH
        )
        self.ontology.load()

    def search_by_type(self, class_name: ClassName) -> list[NamedIndividual]:
        """Restituisce una lista di individui di una classe

        Args:
            class_name (ClassName): Nome della classe da cui cercare gli
            individui

        Returns:
            list[NamedIndividual]: Lista di individui
        """

        return self.ontology.search(
            type=self.ontology[class_name]
        )

    def search_by_subclass(self, class_name: ClassName) -> list[ThingClass]:
        """Restituisce una lista contenente le sottoclassi di una classe

        Args:
            class_name (ClassName): Nome della classe

        Returns:
            list[ThingClass]: Lista di sottoclassi
        """

        return self.ontology.search(
            subclass_of=self.ontology[class_name]
        )

    def search_all(self, class_name: ClassName) -> list:
        """Restituisce le sottoclassi e gli individui di una classe

        Args:
            class_name (ClassName): Nome della classe

        Returns:
            list: Contiene classi e individui
        """

        return self.ontology.search(
            is_a=self.ontology[class_name]
        )

    def get_all_classes(self) -> list:
        return list(
            map(
                lambda c: c.name,
                list(self.ontology.classes())
            )
        )

    def get_all_individuals(self) -> list[Appliance]:
        individuals: list[NamedIndividual] = list(self.ontology.individuals())
        appliances: list[Appliance] = []

        for i in individuals:
            energy_consumption = list(
                map(
                    lambda w: int(w),
                    i.energy_consumption[0].split(", ")
                )
            )

            a = Appliance().category(
                i.is_instance_of[0].name.lower()
            ).name(
                i.appliance_name[0]
            ).energy_consumption(
                energy_consumption
            ).size(
                i.size[0]
            )

            appliances.append(a)

        return appliances

    # TODO: Aggiungere altri metodi per
    # la manipolazione dell'ontologia
