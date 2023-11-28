from typing import Literal, Self

type Size = Literal["small", "medium", "large"]
type EnergyClass = Literal["A", "B", "C", "D", "E", "F"]
type Category = Literal["multimedia", "kitchen", "washing", "cooling", "other"]


class Appliance:
    def __init__(self) -> None:
        self._name: str = ""
        self._energy_consumption: float = 0  # kWh
        self._energy_class: EnergyClass | Literal[""] = ""
        self._size: Size | Literal[""] = ""
        self._category: Category | Literal[""] = ""

    def name(self, name: str) -> Self:
        self._name = name

        return self

    def energy_consumption(self, energy_consumption: float) -> Self:
        self._energy_consumption = energy_consumption

        return self

    def energy_class(self, energy_class: EnergyClass) -> Self:
        self._energy_class = energy_class

        return self

    def size(self, size: Size) -> Self:
        self._size = size

        return self

    def category(self, category: Category) -> Self:
        self._category = category

        return self

    def __str__(self) -> str:
        return (
            f'(Name: {self._name}, '
            f'Energy Consumption: {self._energy_consumption} kWh, '
            f'Energy Class: {self._energy_class}, Size: {self._size}, '
            f'Category: {self._category})'
        )
