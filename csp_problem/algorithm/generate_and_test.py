from itertools import combinations, product

from csp_problem.Constraint import Constraint
from csp_problem.resolver import Resolver
from csp_problem.Variable import Variable


class GenerateAndTest(Resolver):

    def solve(self, variables: list[Variable], constraints: list[Constraint]) -> list:
        valid_assignments = []
        n_variables = len(variables)

        for assignment in product(range(0, n_variables), repeat=n_variables):

            if all(c.evaluate(assignment) for c in constraints):
                valid_assignments.append(assignment)

        return valid_assignments


# return all(
#     con.holds(assignment)
#             for con in self.constraints
#                 if con.can_evaluate(assignment)
# )
