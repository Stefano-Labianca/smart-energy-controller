from typing import Self


class Appliance:
    """Rappresenta un dispositivo elettronico
    """

    def __init__(self) -> None:
        self._name: str = ""
        self._energy_consumption: list[int] = []  # Watt
        self._size: str = ""
        self._category: str = ""

    def name(self, name: str) -> Self:
        """Imposta il nome del dispositivo elettronico

        Args:
            name (str): Nome del dispositivo elettronico

        Returns:
            Self: Istanza della classe con nome aggiornato
        """

        self._name = name

        return self

    def energy_consumption(self, energy_consumption: list[int]) -> Self:
        """Imposta il consumo energetico del dispositivo in watt

        Args:
            energy_consumption (int): Consumo energetico espresso in watt

        Returns:
            Self: Istanza della classe con consumo energetico aggiornato
        """

        self._energy_consumption = energy_consumption

        return self

    def size(self, size: str) -> Self:
        """Imposta le dimensioni del dispositivo elettronico

        Args:
            size (str): Dimensioni del dispositivo elettronico

        Returns:
            Self: Istanza della classe con le dimensioni aggiornate
        """
        self._size = size

        return self

    def category(self, category: str) -> Self:
        """Imposta la categoria del dispositivo elettronico

        Args:
            category (str): Categoria del dispositivo elettronico

        Returns:
            Self: Istanza della classe con la categoria aggiornata
        """
        self._category = category

        return self

    def __str__(self) -> str:
        return (
            f'Appliance => (Name: {self._name}, '
            f'Energy Consumption: {self._energy_consumption} W, '
            f'Size: {self._size}, '
            f'Category: {self._category})'
        )
