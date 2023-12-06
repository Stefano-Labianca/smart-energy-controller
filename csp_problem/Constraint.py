class Constraint:
    def __init__(self, condition, scope: list[str]) -> None:
        self.condition = condition  # funzione booleana
        self.scope = scope

    def __str__(self) -> str:
        return (
            f'Constraint => (Name: {self.condition.__name__}, '
            f'Scope: {self.scope})'
        )

    def evaluate(self, assignment: dict) -> bool:

        # Controllo se posso valutare il mio assegnamento 
        if all(v in assignment for v in self.scope):
            for v in self.scope:
                if not self.condition(assignment[v]):
                    return False
        
        return True



