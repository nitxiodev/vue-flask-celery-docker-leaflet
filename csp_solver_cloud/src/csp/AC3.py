class AC3(object):
    def __init__(self):
        pass

    def ac3(self, csp):
        queue = [(x, y) for x in csp.variables for y in csp.neighbors[x]]

        while queue:
            x_i, x_j = queue.pop()
            if self._revise(csp, x_i, x_j):
                if len(csp.domains[x_i]) == 0:
                    return False
                for x_k in csp.neighbors[x_i] - {x_j}:
                    queue.append((x_k, x_i))

    def _revise(self, csp, x_i, x_j):
        revised = False
        for x in csp.domains[x_i]:
            if not any([csp.constraints(x, y) for y in csp.domains[x_j]]):
                csp.domains[x_i].remove(x)
                revised = True

        return revised
