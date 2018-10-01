import celery
from celery.exceptions import Reject
from flask_socketio import SocketIO

from csp_solver_cloud.src.server import ServiceException
from csp_solver_cloud.src.server.MapService import MapService
from csp_solver_cloud.src.server.flask_inits import app


class MapTask(celery.Task):
    name = __name__
    serializer = 'json'
    ignore_result = False

    def __init__(self):
        self._map_service = MapService()
        super(MapTask, self).__init__()

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super(MapTask, self).__call__(*args, **kwargs)

    def run(self, latitude, longitude, colors, client_id, message_queue, *args, **kwargs):
        self.update_state(state='PROGRESS', meta={})

        # Websockets support
        local_socketio = SocketIO(message_queue=message_queue)

        try:
            solution = self._map_service.solve(latitude, longitude, colors)
            msg = {
                'solution': solution
            }

            local_socketio.emit('mapSol', self.request.id, room=client_id)
            return msg
        except ServiceException as f:
            self.update_state(state='FAILURE', meta={'exc_type': '', 'exc_message': (f.errorcode.value, f.message)})
            local_socketio.emit('mapErr', '{}-{}'.format(f.errorcode.value, f.message), room=client_id)
            raise Reject()
