from flask import Blueprint, jsonify
from flask import request
from kombu.exceptions import OperationalError

from csp_solver_cloud.src.server.Boost import Boost


class AsyncAPI(Blueprint):
    def __init__(self, name, import_name, celery_tasks, celery, spawned, *args):
        self._celery_tasks = celery_tasks
        self._celery = celery
        self._config = None
        self._boost = Boost(spawned)
        super(AsyncAPI, self).__init__(name, import_name, *args)

        @self.route('/map_async', methods=['POST'])
        def map_async():
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
                client_id = data.get('id')

                if client_id is None:
                    ret = {
                        'msg': 'In async mode, client uuid is mandatory',
                        'code': 422
                    }
                else:

                    try:
                        job = self._boost.call(self._celery_tasks.get('map').delay, latitude, longitude, colors,
                                               client_id, self._config['SOCKETIO_BROKER_URL'])

                        ret = {
                            'msg': str(job.id) if job else None,
                            'code': 201
                        }
                    except OperationalError as e:
                        ret = {
                            'msg': e.message,
                            'code': 503
                        }

            code = ret.pop('code')
            return jsonify(ret['msg']), code

        @self.route('/sudoku_async', methods=['POST'])
        def sudoku_async():
            data = request.get_json(silent=True)

            if data is None:
                ret = {
                    'msg': 'Data must be encoded in a JSON object!',
                    'code': 422
                }
            else:
                sudoku = data.get('sudoku')
                client_id = data.get('id')

                if client_id is None:
                    ret = {
                        'msg': 'In async mode, client uuid is mandatory',
                        'code': 422
                    }
                else:
                    try:
                        job = self._boost.call(self._celery_tasks.get('sudoku').delay, sudoku, client_id,
                                               self._config['SOCKETIO_BROKER_URL'])

                        ret = {
                            'msg': str(job.id) if job else None,
                            'code': 201
                        }
                    except OperationalError as e:
                        ret = {
                            'msg': e.message,
                            'code': 503
                        }

            code = ret.pop('code')
            return jsonify(ret['msg']), code

        # Polling of celery tasks
        @self.route('/progress/<task_id>', methods=['GET'])
        def progress(task_id):
            job = self._celery.AsyncResult(task_id)
            result = job.result
            if job.state == 'PENDING':
                ret = {
                    'status': job.state,
                    'msg': {},
                    'code': 404
                }
            elif job.state != 'FAILURE':
                ret = {
                    'status': job.state,
                    'msg': {
                        'solution': result.get('solution')
                    },
                    'code': 200
                }

            else:
                ret = {
                    'status': job.state,
                    'msg': {
                        'code': result[0],
                        'message': result[1]
                    },
                    'code': 400
                }

            code = ret.pop('code')
            return jsonify(ret), code  # change after unittest

    def register(self, app, options, first_registration=False):
        super(AsyncAPI, self).register(app, options, first_registration)
        self._config = app.config
