from gevent.monkey import patch_all

patch_all()

from celery import Celery
from flask import Flask
from flask_socketio import SocketIO
from flask_compress import Compress
from flask_cors import CORS
import os

socketio = SocketIO()
compress = Compress()
cors = CORS()


def createApp(config, socket_io=False):
    app = Flask(__name__)
    app.config.from_object(config)
    compress.init_app(app)

    if socket_io:
        socketio.init_app(app, message_queue=app.config['SOCKETIO_BROKER_URL'])

    return app


# Config mode
DEPLOY_MODE = 'csp_solver_cloud.src.server.config.ProductionConfig'
FLASK_SERVER_PORT = 8888
SOCKETIO_SERVER_PORT = 8000
GEOCODER_TIMEOUT = 60
BOOST = True  # Use gevent.spawn in async mode in order to achieve more requests per sec (up to 5000)
GEOCODER = 'arcgis|photon'.upper()  # photon|arcgis, arcgis|photon, arcgis or photon
IS_GUNICORN = 'gunicorn' in os.environ.get("SERVER_SOFTWARE", "")

# Main Flask app
app = createApp(DEPLOY_MODE)

# Configure celery
celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Main socketio app
socketio_app = createApp(DEPLOY_MODE, socket_io=True) if IS_GUNICORN else None
