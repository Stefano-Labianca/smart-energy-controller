from csp_problem.Constraint import Constraint
from csp_problem.resolver import Resolver
from csp_problem.Variable import Variable


class CSP:
    def __init__(self, variables: list[Variable], constraints: list[Constraint]) -> None:
        self.variables = variables
        self.constraints = constraints

        # E' una mappatura tra il nome della variabile e un vincolo dove:
        # var_to_const[var_name] mi restituisce i vincoli che hanno
        # var_name nello scope
        self.var_to_const = {var.name : set[Constraint]() for var in self.variables}

        for con in constraints:
            for var_name in con.scope:
                self.var_to_const[var_name].add(con)
                

    def solve(self, resolver: Resolver) -> list:
        return resolver.solve(self.variables, self.constraints)
