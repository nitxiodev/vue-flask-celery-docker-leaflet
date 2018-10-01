from abc import ABCMeta, abstractmethod
from csp_solver_cloud.src.csp.AC3 import AC3

UNASSIGNED = None


class CSP(object):
    __metaclass__ = ABCMeta

    def __init__(self, X, D, C, variable_heuristic, domain_heuristic):
        self._X = X
        self._D = D
        self._C = C
        self._variable_heuristic = variable_heuristic
        self._domain_heuristic = domain_heuristic
        self._removed = None
        self._neighbors = {}
        self._ac3 = AC3()

    @property
    def neighbors(self):
        return self._neighbors

    @property
    def variables(self):
        return self._X

    @property
    def domains(self):
        return self._D

    @property
    def constraints(self):
        return self._C

    @abstractmethod
    def build_neighbors(self):
        raise NotImplementedError('Not implemented yet!')

    @abstractmethod
    def solved(self):
        raise NotImplementedError('Not implemented yet!')

    @abstractmethod
    def valid_assignment(self, variable, value):
        raise NotImplementedError('Not implemented yet!')

    def backtracking_search(self):
        self._ac3.ac3(self)  # preprocessing step - arc consistency

        if self.consistent():
            for domain in self.domains:
                self.variables[domain] = self.domains[domain][0]
            has_solution = True
        else:
            self._removed = {key: [] for key in self.variables}
            has_solution = self._backtrack()

        return has_solution

    def _backtrack(self):
        if self.solved():
            return True

        var = self.select_unassigned_variable(self._variable_heuristic)
        for value in self.order_domain_values(var, self._domain_heuristic):
            if self.valid_assignment(var, value):
                self.variables[var] = value
                self.forward_check(var, value)

                result = self._backtrack()
                if result:
                    return result

                self.variables[var] = UNASSIGNED
                for varr, valuee in self._removed[var]:
                    self.domains[varr].append(valuee)
                self._removed[var] = []
        return False

    def forward_check(self, variable, value):
        for neighbor in self.neighbors[variable]:
            if self.variables[neighbor] == UNASSIGNED:  # unassigned variable
                if value in self.domains[neighbor]:
                    self.domains[neighbor].remove(value)
                    self._removed[variable].append([neighbor, value])

    def _minimum_remaining_values(self):
        unassigned_variables = {key: self.domains[key] for key in self.domains if self.variables[key] == UNASSIGNED}
        return min(unassigned_variables, key=lambda x: len(unassigned_variables[x]))

    def _next_unassigned_variable(self):
        for variable in self.variables:
            if self.variables[variable] == UNASSIGNED:
                return variable

    def select_unassigned_variable(self, heuristic='mrv'):
        if heuristic == 'mrv':
            return self._minimum_remaining_values()

        return self._next_unassigned_variable()

    def _least_constraining_values(self, variable):
        domain = {key: 0 for key in self.domains[variable]}

        if len(self.domains[variable]) > 1:
            for neighbor in self.neighbors[variable]:
                for x in self.domains[neighbor]:
                    if x in domain:
                        domain[x] += 1

        return sorted(domain, key=domain.get, reverse=True)

    def _no_heuristic_values(self, variable):
        return self.domains[variable]

    def order_domain_values(self, variable, heuristic='lcv'):
        if heuristic == 'lcv':
            return self._least_constraining_values(variable)

        return self._no_heuristic_values(variable)

    def consistent(self):
        return all(len(self.domains[x]) == 1 for x in self.domains)
