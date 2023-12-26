from ontology.ontology_controller import ApplianceOntology
from ontology.sparql import SPARQL, OWLType

ontology = ApplianceOntology()
query_manager = SPARQL()

query_manager.select(['x']).where(
    [OWLType.NAMED_INDIVIDUAL]
).execute()

# print(ontology.get_all_classes())
# appliances = ontology.get_all_individuals()

# print(
#     ontology.search_by_type("Appliance")
# )


# print(
#     ontology.search_by_subclass("Appliance")
# )


# print(
#     ontology.search_all("Appliance"),
#     ontology.search_all("Cooling"),
#     ontology.search_all("Kitchen"),
#     ontology.search_all("Washing"),
#     ontology.search_all("Multimedia"),
#     ontology.search_all("Other"),
#     sep="\n\n"
# )
