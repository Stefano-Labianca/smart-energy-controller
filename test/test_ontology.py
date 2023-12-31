from rdflib import URIRef
from rich.console import Console

from appliance.Appliance import Appliance
from ontology.appliance_ontology import ApplianceOntology

ontology = ApplianceOntology()
console = Console()


appliances = ontology.create_appliance()

for a in appliances:
    console.print(a)
