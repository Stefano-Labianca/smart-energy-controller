from abc import ABC, abstractmethod


class Resolver(ABC):
    def __init__(self, domain: list[int], amount: int) -> None:
        self.domain = domain
        self.amount = amount

    @abstractmethod
    def solve(self) -> list:
        raise NotImplementedError
