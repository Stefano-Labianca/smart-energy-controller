from rich.console import Console
from rich.table import Table

from csp_problem.Constraint import Constraint
from csp_problem.Variable import Variable

console = Console()


def variables_printer(variables: list[Variable]) -> None:
    table = Table(title="Variables")
    table.add_column("Name", style="green")
    table.add_column("Domain", style="cyan")

    for v in variables:
        table.add_row(v.name, v.domain.__str__())
        table.add_section()

    console.print(table)


def constraints_printer(constraints: list[Constraint]) -> None:
    table = Table(title="Constraints")

    table.add_column("Condition", style="green")
    table.add_column("Scope", style="cyan")

    for c in constraints:
        table.add_row(c.condition.__name__, ", ".join(c.scope))
        table.add_section()

    console.print(table)


def assignments_printer(assignments: list[dict[str, int]]) -> None:
    table = Table(title="Total Assignments")

    for v_name in assignments[0]:
        table.add_column(v_name, style="cyan")

    for a in assignments:
        values = tuple(
            map(
                lambda v: str(v),
                tuple(a.values())
            )
        )

        table.add_row(*values, style="green")
        table.add_section()

    console.print(table)
