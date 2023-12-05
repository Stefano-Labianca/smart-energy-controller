from csp.resolver import Resolver


class GenerateAndTest(Resolver):

    def __init__(self, domain: list[int], constraints: list) -> None:
        super().__init__(domain, constraints)

    def solve(self) -> list:
        return []
