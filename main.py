from rdflib import URIRef

from appliance.Appliance import Appliance
from appliance.appliances_controller import create_appliances
from ontology.ontology_controller import ApplianceOntology

ontology = ApplianceOntology()


def test_add():
    a = Appliance().name("fryer").category(
        "Kitchen").size("medium").energy_consumption([200])

    ontology.add(a)
    ontology.save()


def test_remove():
    ontology.remove(
        URIRef('http://www.semanticweb.org/utente/ontologies/2023/11/appliances#fryer')
    )

    ontology.save()


# test_add()
# test_remove()

ontology.show()
