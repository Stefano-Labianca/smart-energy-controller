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


def partial_assignments_printer(assignments: list[dict[str, int]], variables_name: list[str]) -> None:
    print("\n")
    table = Table(title="Partials Assignments")
    rows: list[dict[str, str]] = []
    can_insert = False

    for name in variables_name:
        table.add_column(name, style="cyan")

    for assignment in assignments:
        p_assignment: dict[str, str] = {}

        for name in assignment:
            if name in variables_name:
                p_assignment[name] = str(assignment[name])

        if len(rows) > 0:
            can_insert = all(p_assignment != r for r in rows)

        if can_insert or len(rows) == 0:
            table.add_row(*p_assignment.values(), style="green")
            table.add_section()

            rows.append(p_assignment)

    console.print(table)


def assignments_printer(assignments: list[dict[str, int]]) -> None:
    print("\n")
    table = Table(title="Total Assignments")
    names = assignments[0].keys()

    for name in names:
        table.add_column(name, style="cyan")

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


def query_result_printer(result: list[list], variables: list[str]) -> None:
    print("\n")
    table = Table(title="Query Result", )

    for column in variables:
        table.add_column(column, justify="center")

    for row in result:
        table.add_row(row[0].name, style='blue')
        table.add_section()

    console.print(table)
