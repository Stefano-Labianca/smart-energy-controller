from enum import StrEnum

from experta import DefFacts, Fact, KnowledgeEngine, Rule
from rich.console import Console

from cli.user_cli import UserCLI
from ontology.appliance_ontology import ApplianceOntology

console = Console()


WARNING_THRESHOLD = 150


class StatusEnum(StrEnum):
    DOWN = "down"
    WARNING = "warning"
    UP = "up"


class ExpertSystem(KnowledgeEngine):
    """Sistema esperto usato per determinare quali dispositivi
    elettronici, accessi contemporaneamente, possono far saltare il 
    contatore elettrico.
    """

    def __init__(self, max_usage: float) -> None:
        super().__init__()

        self.ontology = ApplianceOntology()
        self.max_usage = max_usage
        self.selected_appliances: list[dict[str, list[int]]] = []

    @DefFacts()
    def _initial_action(self):
        """Azione iniziale del sistema esperto.
        L'azione iniziale è quella di inizializzare i fatti
        del sistema esperto.
        """

        yield Fact(action="init")
        yield Fact(action="start")

    @Rule(Fact(action="init"), salience=2)
    def init_system(self):
        """Inizializza il sistema esperto usando come fatti il 
        consumo energetico degli elettrodomestici contenuti nell'ontologia.
        """

        appliances = self.ontology.create_appliances()

        for a in appliances:
            for e in a._energy_consumption:
                self.declare(
                    Fact(consumption={a._name: e})
                )

    @Rule(Fact(action="start"))
    def start_system(self):
        """Avvia il sistema esperto
        """

        self.selected_appliances = UserCLI.choose_appliances()
        output_status = self.check_power()

        self.declare(Fact(status=output_status))

    @Rule(Fact(status="down"))
    def power_is_out(self):
        """Viene eseguita nel caso in cui, i dispositivi in uso o che si vogliono 
        usare faranno scattare il salvavita
        """

        console.print(
            "\nAttenzione!, accendendo i dispositivi scelti rischi di far saltare il salvavita!\n",
            style="red"
        )

        t_max = 0
        max_w = 0
        name = ""

        for a in self.selected_appliances:
            for p in a.values():
                t_max = max(p)

                if t_max > max_w:
                    name = list(a.keys())[0]
                    max_w = t_max

        console.print(
            f"Consiglio di spegenere il seguente dispositivo: "
            f"{name}, in quando consuma {max_w} Wh\n"
        )

    @Rule(Fact(status="warning"))
    def power_can_go_out(self):
        """Viene eseguita nel caso si raggiunga una certa soglia
        in cui è possibile che il salvavita possa scattare, a causa di
        un improvviso aumento del consumo.
        """

        t_max = 0
        max_w = 0
        name = ""

        for a in self.selected_appliances:
            for p in a.values():
                t_max = max(p)

                if t_max > max_w:
                    name = list(a.keys())[0]
                    max_w = t_max

        console.print(
            (
                f"\nUn uso prolungato dell seguente dispositivo {name}, "
                f"con consumo di {max_w} W, "
                f"potrebbe far scattare il salvavita, a causa ad un improvviso "
                f"aumento dei consumi.\n"
            ),
            style="yellow"
        )

    @Rule(Fact(status="up"))
    def power_is_safe(self):
        """Viene eseguita quando il salvavita non potrà scattare con i dispositivi
        in uso
        """

        console.print("\nTutto sotto controllo!\n", style="green")

    def check_power(self) -> str:
        """Verifica se i dispositivi che si vogliono avviare
        possono far saltare il salvavita

        Returns:
            str: Stato del sistema
        """
        threshold = self.max_usage * 1000
        energy_sum = 0

        for appliance in self.selected_appliances:
            for power in appliance.values():
                energy_sum += sum(power)

        if abs(threshold - energy_sum) <= WARNING_THRESHOLD:
            return StatusEnum.WARNING

        if energy_sum > threshold:
            return StatusEnum.DOWN

        return StatusEnum.UP


def run_expert_system(max_usage: float):
    """Permette l'avvio del sistema esperto dall'esterno
    """

    expert_system = ExpertSystem(max_usage)

    expert_system.reset()
    expert_system.run()

    # print(expert_system.facts)
