from experta import DefFacts, Fact, KnowledgeEngine, Rule

from ontology.appliance_ontology import ApplianceOntology


class ExpertSystem(KnowledgeEngine):
    def __init__(self, ontology: ApplianceOntology) -> None:
        super().__init__()
        self.ontology = ontology

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="init")
        # yield Fact(consumption={"laptop": 300})

    @Rule(Fact(action="init"), salience=2)
    def init_system(self):
        """Inizializza il sistema esperto usando come fatti il 
        consumo energetico degli elettrodomestici contenuti nell'ontologia
        """
        appliances = self.ontology.create_appliances()

        for a in appliances:
            for e in a._energy_consumption:
                self.declare(
                    Fact(consumption={a._name: e})
                )

    # @Rule(Fact(consumption={"laptop": 300}))
    # def prova(self):
    #     print("Laptop")


def run_expert_system(ontology: ApplianceOntology):
    """Esegue il sistema esperto
    """
    expert_system = ExpertSystem(ontology)

    expert_system.reset()
    expert_system.run()

    print(expert_system.facts)
