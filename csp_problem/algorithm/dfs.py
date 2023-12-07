from csp_problem.Constraint import Constraint
from csp_problem.resolver import Resolver
from csp_problem.Variable import Variable


class DFS(Resolver):

    def solve(self, variables: list[Variable], constraints: list[Constraint]):
        return list(self.__dfs(variables, constraints))

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
