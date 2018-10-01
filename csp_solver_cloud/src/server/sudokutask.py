import celery
from celery.exceptions import Reject
from flask_socketio import SocketIO

from csp_solver_cloud.src.server import ServiceException
from csp_solver_cloud.src.server.SudokuService import SudokuService
from csp_solver_cloud.src.server.flask_inits import app


class SudokuTask(celery.Task):
    name = __name__
    serializer = 'json'
    ignore_result = False

    def __init__(self):
        self._sudoku_service = SudokuService()
        super(SudokuTask, self).__init__()

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super(SudokuTask, self).__call__(*args, **kwargs)

    def run(self, sudoku, client_id, message_queue, *args, **kwargs):
        self.update_state(state='PROGRESS', meta={})

        # Websockets support
        local_socketio = SocketIO(message_queue=message_queue)

        try:
            solution = self._sudoku_service.solve(sudoku)
            msg = {
                'solution': solution
            }

            local_socketio.emit('sudokuSol', msg, room=client_id)
            return msg
        except ServiceException as f:
            self.update_state(state='FAILURE', meta={'exc_type': '', 'exc_message': (f.errorcode.value, f.message)})
            local_socketio.emit('sudokuErr', '{}-{}'.format(f.errorcode.value, f.message), room=client_id)
            raise Reject()
