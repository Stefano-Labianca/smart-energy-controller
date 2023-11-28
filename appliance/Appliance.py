from typing import Self


class Appliance:
    def __init__(self) -> None:
        self._name: str = ""
        self._energy_consumption: int = 0  # kWh/anno
        self._energy_class: str = ""
        self._size: str = ""
        self._category: str = ""

    def name(self, name: str) -> Self:
        self._name = name

        return self

    def energy_consumption(self, energy_consumption: int) -> Self:
        self._energy_consumption = energy_consumption

        return self

    def energy_class(self, energy_class: str) -> Self:
        self._energy_class = energy_class

        return self

    def size(self, size: str) -> Self:
        self._size = size

        return self

    def category(self, category: str) -> Self:
        self._category = category

        return self

    def __str__(self) -> str:
        return (
            f'(Name: {self._name}, '
            f'Energy Consumption: {self._energy_consumption} kWh, '
            f'Energy Class: {self._energy_class}, Size: {self._size}, '
            f'Category: {self._category})'
        )
