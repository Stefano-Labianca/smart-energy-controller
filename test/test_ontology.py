from rdflib import URIRef
from rich.console import Console

from appliance.Appliance import Appliance
from ontology.appliance_ontology import ApplianceOntology, URIEnum

ontology = ApplianceOntology()
console = Console()


def test_create_ontology():
    appliances = ontology.create_appliances()

    for a in appliances:
        console.print(a)


def test_show():
    ontology.show()


def test_add_and_save():
    a = Appliance().name("test_appliance").category(
        "Other").size("small").energy_consumption([10])

    ontology.add(a)
    ontology.save()


def test_remove():
    ontology.remove(URIRef(
        URIEnum.URI_BASE + "test_appliance"
    ))


def test_contains():
    print(ontology.find(URIRef(
        URIEnum.URI_BASE + "test_appliance"
    )))


def test_find():
    ontology.find(URIRef(
        URIEnum.URI_BASE + "test_appliance"
    ))


# test_create_ontology()
# test_show()
# test_add_and_save()
# test_remove()
# test_contains()
# test_find()
