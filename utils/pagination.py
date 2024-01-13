from itertools import batched

from rich.console import Console

from utils.printer import assignments_printer, partial_assignments_printer

console = Console()


class Pagination:
    """Classe di supporto usata per mostrare sul terminale tutti gli assegnamenti 
    determinati dagli algoritmi del CSP
    """

    def __init__(self, elements: list[dict[str, int]], size: int = 20) -> None:
        """Inizializza la paginazione

        Args:
            elements (list[dict[str, int]]): Assegnazioni determinate dal CSP
            size (int, optional): Numero di elementi in una pagina. Di default ho 20 elementi per pagina
        """

        self.current_page = 0
        self.content = list(batched(elements, size))

    def show_total(self):
        """Mostra gli elementi della pagina corrente, in termini di 
        assegnamenti totali
        """

        assignments_printer(
            list(self.content[self.current_page])
        )

        console.print(
            f'Pagina corrente: {self.current_page + 1}',
            justify="center"
        )

        console.print(f'Premi 1 per andare alla pagina successiva')
        console.print(f'Premi 0 per andare alla pagina precedente')

    def show_partial(self, variables_names: list[str]):
        """Mostra gli elementi della pagina corrente, in termini di 
        assegnamenti parziali
        """
        partial_assignments_printer(
            list(self.content[self.current_page]),
            variables_names
        )

        console.print(
            f'Pagina corrente: {self.current_page + 1}',
            justify="center"
        )

        console.print(f'Premi 1 per andare alla pagina successiva')
        console.print(f'Premi 0 per andare alla pagina precedente')

    def next_page(self) -> None:
        """Porta alla pagina successiva
        """

        if self.current_page < len(self.content) - 1:
            self.current_page += 1
        else:
            self.current_page = 0

    def previous_page(self) -> None:
        """Porta alla pagina precedente
        """

        if self.current_page > 0:
            self.current_page -= 1
        else:
            self.current_page = len(self.content) - 1
