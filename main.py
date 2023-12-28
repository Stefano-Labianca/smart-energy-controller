from rdflib import URIRef
from rich.console import Console

from appliance.Appliance import Appliance
from ontology.appliance_ontology import ApplianceOntology

ontology = ApplianceOntology()
console = Console()


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


def test_contains():
    print(ontology.contains(
        URIRef('http://www.semanticweb.org/utente/ontologies/2023/11/appliances#fryer')
    ))

    print(ontology.contains(
        URIRef('http://www.semanticweb.org/utente/ontologies/2023/11/appliances#computer')
    ))


def test_find():

    triples = ontology.find(
        URIRef(
            'http://www.semanticweb.org/utente/ontologies/2023/11/appliances#computer')
    )

    console.print(triples)


# test_add()
# test_remove()
# test_contains()
# test_find()

appliances = ontology.create_appliance()

for a in appliances:
    console.print(a)
