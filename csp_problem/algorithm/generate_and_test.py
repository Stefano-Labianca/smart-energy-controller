from itertools import combinations, product

from csp_problem.Constraint import Constraint
from csp_problem.resolver import Resolver
from csp_problem.Variable import Variable


class GenerateAndTest(Resolver):

    def solve(self, variables: list[Variable], constraints: list[Constraint]) -> list:
        valid_assignments = []
        n_variables = len(variables)
        assignment = {}

        for comb in product(range(0, n_variables), repeat=n_variables):
            v_idx = 0

            # Creo un assegnamento
            for idx in comb:
                v = variables[v_idx]
                assignment[v.name] = v.domain[idx]

                v_idx += 1

            if all(c.evaluate(assignment) for c in constraints):
                valid_assignments.append(assignment)

                print(assignment)

        return valid_assignments