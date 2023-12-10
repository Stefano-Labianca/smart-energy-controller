from csp_problem.Constraint import Constraint
from csp_problem.csp import CSP
from csp_problem.resolver import Resolver
from csp_problem.Variable import Variable


class DFS:

    def __init__(self, csp: CSP) -> None:
        self.variables = csp.variables
        self.constraints = csp.constraints

    def solve(self):
        return list(self.__dfs(self.variables, self.constraints))

    def __dfs(self, variables: list[Variable], constraints: list[Constraint], context={}):
        eval_cons = {c for c in constraints if c.can_evaluate(context)}

        if all(c.evaluate(context) for c in eval_cons):
            if len(variables) == 0:
                yield context
            else:
                remaining_cons = [c for c in constraints if c not in eval_cons]
                variable = variables[0]

                for value in variable.domain:
                    yield from self.__dfs(
                        variables[1:],
                        remaining_cons,
                        context | {variable.name: value}
                    )
