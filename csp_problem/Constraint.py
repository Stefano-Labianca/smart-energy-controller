class Constraint:
    def __init__(self, condition, scope: list[str]) -> None:
        self.condition = condition
        self.scope = scope

    def __str__(self) -> str:
        return (
            f'Constraint => (Name: {self.condition.__name__}, '
            f'Scope: {self.scope})'
        )

    def can_evaluate(self, assignment: dict[str, int]) -> bool:
        for v in self.scope:
            if v not in assignment:
                return False
        return True

    def evaluate(self, assignment: dict) -> bool:

        restricted_assignment = {}

        for v in self.scope:
            restricted_assignment[v] = assignment[v]

        if len(restricted_assignment) == 0:
            return False

        return self.condition(restricted_assignment)
