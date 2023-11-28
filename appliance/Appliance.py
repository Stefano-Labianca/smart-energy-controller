from typing import Self


class Appliance:
    """Rappresenta un elettrodomestico
    """

    def __init__(self) -> None:
        self._name: str = ""
        self._energy_consumption: int = 0  # kWh/anno
        self._energy_class: str = ""
        self._size: str = ""
        self._category: str = ""

    def name(self, name: str) -> Self:
        """Imposta il nome dell'elettrodomestico

        Args:
            name (str): Nome dell'elettrodomestico

        Returns:
            Self: Istanza della classe con nome aggiornato
        """

        self._name = name

        return self

    def energy_consumption(self, energy_consumption: int) -> Self:
        """Imposta il livello di consumo annuno in kWh

        Args:
            energy_consumption (int): Consumo annuo in kWh

        Returns:
            Self: Istanza della classe con consumo energetico annuo aggiornato
        """

        self._energy_consumption = energy_consumption

        return self

    def energy_class(self, energy_class: str) -> Self:
        """Imposta la classe energetica dell'elettrodomestico

        Args:
            energy_class (str): Classe energetica dell'elettrodomestico

        Returns:
            Self: Istanza della classe con classe energetica aggiornata
        """

        self._energy_class = energy_class

        return self

    def size(self, size: str) -> Self:
        """Imposta le dimensioni dell'elettrodomestico

        Args:
            size (str): Dimensioni dell'elettrodomestico

        Returns:
            Self: Istanza della classe con le dimensioni aggiornate
        """
        self._size = size

        return self

    def category(self, category: str) -> Self:
        """Imposta la categoria dell'elettrodomestio

        Args:
            category (str): Categoria dell'elettrodomestio

        Returns:
            Self: Istanza della classe con la categoria aggiornata
        """
        self._category = category

        return self

    def __str__(self) -> str:
        return (
            f'(Name: {self._name}, '
            f'Energy Consumption: {self._energy_consumption} kWh, '
            f'Energy Class: {self._energy_class}, Size: {self._size}, '
            f'Category: {self._category})'
        )
