from types import FunctionType


class Constraint:
    def __init__(self, condition) -> None:
        self.condition = condition  # funzione booleana

    def __str__(self) -> str:
        return f'Constraint => (Name: {self.condition.__name__})'

    def evaluate(self, assignment: tuple | list) -> bool:
        return self.condition(*assignment)
