from flask import request
from flask_socketio import emit
from csp_solver_cloud.src.server.flask_inits import socketio, SOCKETIO_SERVER_PORT, DEPLOY_MODE, createApp, socketio_app


@socketio.on('connect')
def connect(*sid):
    print('Connected ', request.sid)


@socketio.on('disconnect')
def disconnect(*sid):
    print('Disconnected ', request.sid)


@socketio.on('my_id')
def my_id():
    emit('connected', request.sid)


if __name__ == '__main__':
    try:
        socketio_app = createApp(DEPLOY_MODE, socket_io=True)
        socketio.run(socketio_app, host='0.0.0.0', port=SOCKETIO_SERVER_PORT)
    except KeyboardInterrupt:
        socketio.stop()
