from flask import Blueprint, jsonify
from flask import request

from csp_solver_cloud.src.server import ServiceException, ServiceCodes
from csp_solver_cloud.src.server.MapService import MapService
from csp_solver_cloud.src.server.SudokuService import SudokuService


class SyncAPI(Blueprint):
    def __init__(self, *args):
        self._map_service = MapService()
        self._sudoku_service = SudokuService()
        self._config = None
        super(SyncAPI, self).__init__(*args)

        @self.route('/map_sync', methods=['POST'])
        def solver():
            data = request.get_json(silent=True)

            if data is None:
                ret = {
                    'msg': 'Data must be encoded in a JSON object!',
                    'code': 422
                }
            else:
                latitude = data.get('lat')
                longitude = data.get('long')
                colors = data.get('colors')

                try:
                    solution = self._map_service.solve(latitude, longitude, colors)
                    ret = {
                        'msg': {
                            'solution': solution
                        },
                        'code': 200
                    }
                except ServiceException as f:
                    if f.errorcode == ServiceCodes.EMPTY_PARAMS:
                        ret = {
                            'msg': 'Some or every parameters are empty!',
                            'code': 422
                        }
                    else:
                        ret = {
                            'msg': f.message,
                            'code': 409
                        }
            code = ret.pop('code')
            return jsonify(ret['msg']), code

        @self.route('/sudoku_sync', methods=['POST'])
        def sudoku_solver():
            data = request.get_json(silent=True)

            if data is None:
                ret = {
                    'msg': 'Data must be encoded in a JSON object!',
                    'code': 422
                }
            else:
                sudoku = data.get('sudoku')

                try:
                    solution = self._sudoku_service.solve(sudoku)
                    ret = {
                        'msg': {
                            'solution': solution
                        },
                        'code': 200
                    }
                except ServiceException as f:
                    if f.errorcode == ServiceCodes.EMPTY_PARAMS:
                        ret = {
                            'msg': 'Some or every parameters are empty!',
                            'code': 422
                        }
                    else:
                        ret = {
                            'msg': f.message,
                            'code': 409
                        }
            code = ret.pop('code')
            return jsonify(ret['msg']), code

    def register(self, app, options, first_registration=False):
        super(SyncAPI, self).register(app, options, first_registration)
        self._config = app.config
