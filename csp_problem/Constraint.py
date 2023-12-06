class Constraint:
    def __init__(self, condition, scope: list) -> None:
        self.condition = condition  # funzione booleana
        self.scope = scope

    def __str__(self) -> str:
        return (
            f'Constraint => (Name: {self.condition.__name__}, '
            f'Scope: {self.scope})'
        )

    def evaluate(self, assignment: tuple | list) -> bool:
        return self.condition(*assignment)
