from csp_problem.Constraint import Constraint
from csp_problem.Variable import Variable


class GAC:
    def __init__(self, variables: list[Variable], constraints: list[Constraint]) -> None:
        self.variables = variables
        self.constraints = constraints
        self.var_to_const = {var.name: set() for var in self.variables}

    def make_arc_consistent(self, domains=None, to_do=None):
        for con in self.constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

        if domains is None:
            self.domains = {var.name: var.domain for var in self.variables}
        else:
            self.domains = domains.copy()

        if to_do is None:
            self.to_do = {
                (var, const)
                for const in self.constraints
                for var in const.scope
            }

        else:
            self.to_do = to_do.copy()

        while self.to_do:
            var, const = self.select_arc()
            other_vars = [ov for ov in const.scope if ov != var]

            new_domain = [
                value for value in self.domains[var]
                if self.any_holds(self.domains, const, {var: value}, other_vars)
            ]

            if new_domain != self.domains[var]:
                add_to_do = self.new_to_do(var, const) - self.to_do

                self.domains[var] = new_domain
                self.to_do |= add_to_do

        return self.domains

    def select_arc(self):
        """Seleziono, elimino e restituisco un arco

        Returns:
            tuple[str, Constraint]: Arco eliminato
        """
        return self.to_do.pop()

    def any_holds(self, domains: dict[str, list[int]], const: Constraint, env: dict[str, int], other_vars: list[str], ind: int = 0):
        """Restituisce True se il vincolo `const` è valido per un assegnamento
        che estende `env` con le variabili di `other_vars`, contenute da `ind` a len(other_vars)

        Args:
            domains (dict[str, list[int]]): Dominio
            const (Constraint): Vincolo da verificare
            env (dict[str, int]): Estensione di un assegnamento
            other_vars (list[str]): Contiene altre variabili
            ind (int, optional): Indice da cui prendere le altre variabili e, di defaults, parte da 0.

        Returns:
            bool: Esito della valutazione del vincolo sull'estensione
        """
        if ind == len(other_vars):
            return const.evaluate(env)

        var = other_vars[ind]

        for val in domains[var]:
            if self.any_holds(domains, const, env | {var: val}, other_vars, ind + 1):
                return True
        return False

    def new_to_do(self, var: str, const: Constraint | None):
        """_summary_

        Args:
            var (str): _description_
            const (Constraint | None): Se è None, allora aggiungi tutti

        Returns:
            _type_: _description_
        """
        return {
            (nvar, nconst) for nconst in self.var_to_const[var]
            if nconst != const
            for nvar in nconst.scope
            if nvar != var
        }

    def solve(self):
        return list(self.generate_solutions())

    def generate_solutions(self, domains=None, to_do=None, context={}):
        new_domains = self.make_arc_consistent(domains, to_do)

        if any(len(new_domains[var]) == 0 for var in new_domains):
            print("Nessuna soluzione")

            return False

        if all(len(new_domains[var]) == 1 for var in new_domains):
            s = []
            for variable in new_domains:
                s.append({variable: new_domains[variable][0]})

            yield s
        else:
            variable = self.select_variable(new_domains)

            if variable:
                d1, d2 = self.split_domain(new_domains[variable.name])

                new_d1 = new_domains | {variable.name: d1}
                new_d2 = new_domains | {variable.name: d2}

                self.to_do = self.new_to_do(variable.name, None)

                yield from self.generate_solutions(new_d1, to_do, context | {variable.name: d1})
                yield from self.generate_solutions(new_d2, to_do, context | {variable.name: d2})

    def select_variable(self, new_domains: dict[str, list[int]]):
        """Seleziono la prima variabile che ha cardinalità del 
        dominio maggiore di 1

        Args:
            new_domains (dict[str, list[int]]): Domini consistenti

        Returns:
            Variable: Variabile v tale che `|dom(v)| > 1`
        """
        for v in self.variables:
            if len(new_domains[v.name]) > 1:
                return v

    def split_domain(self, domain: list[int]) -> tuple[list[int], list[int]]:
        half = len(domain) // 2
        return domain[:half], domain[half:]
