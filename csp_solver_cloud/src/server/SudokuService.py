from csp_solver_cloud.src.server.BaseService import BaseService
from csp_solver_cloud.src.sudoku.Sudoku import Sudoku
from csp_solver_cloud.src.server import ServiceException, ServiceCodes


class SudokuService(BaseService):
    def __init__(self):
        pass

    def solve(self, sudoku):
        if sudoku is None:
            raise ServiceException(ServiceCodes.EMPTY_PARAMS, msg='Empty parameters')

        if len(sudoku) != 81:
            raise ServiceException(ServiceCodes.BAD_PARAMS,
                                   msg='Sudoku grid must have 81 cells, not {}'.format(len(sudoku)))

        sdk = Sudoku(sudoku, 'mrv', 'lcv')
        if sdk.backtracking_search():
            return "".join([str(sdk.variables[key]) for key in sorted(sdk.variables)])

        return None
