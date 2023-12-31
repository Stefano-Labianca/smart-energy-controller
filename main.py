from rdflib import URIRef
from rich.console import Console

from appliance.Appliance import Appliance
from knowledge_base.expert_system import run_expert_system
from ontology.appliance_ontology import ApplianceOntology

ontology = ApplianceOntology()

run_expert_system(ontology)
