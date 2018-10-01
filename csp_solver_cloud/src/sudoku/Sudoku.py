from csp_solver_cloud.src.csp.CSP import CSP, UNASSIGNED
from builtins import range as xrange


class Sudoku(CSP):
    def __init__(self, sudoku, variable_heuristic, domain_heuristic):
        sudoku_domains = {}
        for idx, value in enumerate(sudoku):
            value = int(value)
            row = idx // 9
            col = idx % 9
            sudoku_domains['{}_{}'.format(chr(row + 65), col)] = [value] if value > 0 else [x for x in xrange(1, 10)]

        sudoku_variables = {key: UNASSIGNED for key in sudoku_domains}
        sudoku_constraints = lambda x, y: x != y

        super(Sudoku, self).__init__(sudoku_variables, sudoku_domains, sudoku_constraints,
                                     variable_heuristic, domain_heuristic)
        self.build_neighbors()

    def solved(self):
        return all([self.variables[v] != UNASSIGNED for v in self.variables])

    def valid_assignment(self, variable, value):
        variable_neighbors = self.neighbors[variable]
        return all([self.variables[neighbor] != value for neighbor in variable_neighbors])

    def build_neighbors(self):
        for var in self.variables:
            self._neighbors[var] = set(self._row_neighbors(var) + self._col_neighbors(var) + self._box_neighbors(var))

    ###### HELPER FUNCTIONS
    def _row_neighbors(self, v):
        row, col = v.split('_')
        neighbors = []
        for i in xrange(9):
            if (i + 65) != ord(row):
                neighbors.append('{}_{}'.format(chr(i + 65), col))

        return neighbors

    def _col_neighbors(self, v):
        row, col = v.split('_')
        neighbors = []
        for i in xrange(9):
            if i != int(col):
                neighbors.append('{}_{}'.format(row, i))

        return neighbors

    def _box_neighbors(self, v):
        row, col = v.split('_')
        _row = int((ord(row) - 65) // 3)
        _col = int(int(col) // 3)
        neighbors = []

        for i in xrange(3 * _row, 3 * _row + 3):
            for j in xrange(3 * _col, 3 * _col + 3):
                excluded_cell = '{}_{}'.format(chr(i + 65), j)
                if v != excluded_cell:
                    neighbors.append('{}_{}'.format(chr(i + 65), j))

        return neighbors

    def pretty_print(self):
        pretty_sol = '    \033[4m1\033[0m \033[4m2\033[0m \033[4m3\033[0m \033[4m4\033[0m \033[4m5\033[0m ' \
                     '\033[4m6\033[0m \033[4m7\033[0m \033[4m8\033[0m \033[4m9\033[0m\n'
        for i, s in enumerate(sorted(self.variables)):
            if ((i + 1) % 9) == 1:
                pretty_sol += '{} | '.format(s.split('_')[0])
            pretty_sol += '{} '.format(self.variables[s])
            if ((i + 1) % 9) == 0:
                pretty_sol += '\n'
        return pretty_sol
