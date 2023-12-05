from csp_problem.resolver import Resolver


class CSP:

    def solve(self, resolver: Resolver) -> list:
        return resolver.solve()
