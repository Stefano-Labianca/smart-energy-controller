class Variable:

    def __init__(self, name: str, domain: list[int]) -> None:
        self.name = name
        self.domain = domain

    def __str__(self) -> str:
        return (
            f'Variable => (Name: {self.name}, '
            f'Domain: {self.domain.__str__()})'
        )
