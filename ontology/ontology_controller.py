import os

from owlready2 import ThingClass, get_ontology, onto_path
from owlready2.individual import NamedIndividual

from appliance.Appliance import Appliance


class ApplianceOntology:
    def __init__(self) -> None:
        onto_path.append(".")

        self.ontology = get_ontology("./ontology/appliance_ontology.rdf")
        self.ontology.load()

    def search(self):
        """Cerca qualcosa
        TODO: Si può fate un API molto carina
        """

        print(
            self.ontology.search(
                subclass_of=self.ontology["Appliance"]
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
