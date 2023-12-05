from abc import ABC, abstractmethod


class Resolver(ABC):
    def __init__(self, domain: list[int], constraints: list) -> None:
        self.domain = domain
        self.constraints = constraints

    @abstractmethod
    def solve(self) -> list:
        raise NotImplementedError
