from csp.resolver import Resolver


class CSP:

    def solve(self, resolver: Resolver) -> list:
        return resolver.solve()
