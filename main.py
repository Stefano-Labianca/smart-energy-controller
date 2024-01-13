from rich.console import Console

from cli.ontology_cli import OntologyCLI
from knowledge_base.expert_system import run_expert_system
from project_test.test_csp import execute_csp_problem


def execute_expert_system():
    retry: bool = True

    while True:
        try:
            if retry:
                console.print(
                    "\n\n\n\nInserire il limite massimo del salvavita, espresso in kWh",
                    style="blue"
                )

                max_capacity: float = float(input("> "))
                run_expert_system(max_capacity)

            retry = False
            console.print(
                "\n\n\n\nVuole continuare a testare? (Y/n)",
                style="blue"
            )

            choose: str = input("> ").lower().strip(" ")

            match choose:
                case "y":
                    retry = True
                case "n":
                    break
                case _:
                    console.print("Scelta non valida, riprovare", style="red")

        except ValueError:
            console.print("Valore non corretto, riprovare", style="red")


def execute_ontology():
    while True:
        console.print(
            "Premi 1 mostrare il contenuto dell'ontologia",
            style="blue"
        )
        console.print(
            "Premi 2 per aggiungere un nuovo individuo",
            style="blue"
        )
        console.print(
            "Premi 3 per eliminare un individuo",
            style="blue"
        )

        console.print(
            "Premi 4 per salvare permanentemente gli individui aggiunti",
            style="blue"
        )

        console.print(
            "Premi 5 per cercacre un individuio dal nome",
            style="blue"
        )

        console.print(
            "Premi 6 per verificare la presenza di un individuio dal nome",
            style="blue"
        )

        console.print(
            "\nPer uscire premi 7\n",
            style="blue"
        )

        try:
            choose: int = int(input("> "))

            match choose:
                case 1:
                    OntologyCLI.show()
                    console.print("\n\n\n\n\n\n")
                case 2:
                    OntologyCLI.add()
                    console.print("\n\n\n\n\n\n")
                case 3:
                    OntologyCLI.remove()
                    console.print("\n\n\n\n\n\n")
                case 4:
                    OntologyCLI.save()
                    console.print("\n\n\n\n\n\n")
                case 5:
                    OntologyCLI.find()
                    console.print("\n\n\n\n\n\n")
                case 6:
                    OntologyCLI.contains()
                    console.print("\n\n\n\n\n\n")
                case 7:
                    break
        except ValueError:
            console.print("Valore non corretto, riprovare", style="red")


console = Console()
show_instruction = True

while True:
    if show_instruction:
        console.print("Premi 1 per avviare il CSP", style="blue")
        console.print(
            "Premi 2 per lavorare sull'ontologia",
            style="blue"
        )
        console.print(
            "Premi 3 per avviare il sistema esperto",
            style="blue"
        )
        console.print(
            "\nPer uscire premi 4\n",
            style="blue"
        )

    show_instruction = False

    try:
        choose: int = int(input("> "))

        match choose:
            case 1:
                execute_csp_problem()

                show_instruction = True
                console.print("\n\n\n\n\n\n")
            case 2:
                execute_ontology()

                show_instruction = True
                console.print("\n\n\n\n\n\n")
            case 3:
                execute_expert_system()

                show_instruction = True
                console.print("\n\n\n\n\n\n")
            case 4:
                break

    except ValueError:
        console.print("Valore non corretto, riprovare", style="red")
