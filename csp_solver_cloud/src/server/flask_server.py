from gevent.monkey import patch_all

patch_all()

from csp_solver_cloud.src.server.async_api import AsyncAPI
from csp_solver_cloud.src.server.flask_inits import celery, FLASK_SERVER_PORT, BOOST, app, compress, cors
from csp_solver_cloud.src.server.sync_api import SyncAPI
from csp_solver_cloud.src.server.maptask import MapTask
from csp_solver_cloud.src.server.sudokutask import SudokuTask
from gevent.pywsgi import WSGIServer
from flask import jsonify

# Instance and register every task
map_task = MapTask()
sudoku_task = SudokuTask()
celery.register_task(map_task)
celery.register_task(sudoku_task)

# Import blueprints
sync_api = SyncAPI('sync_api', __name__)
async_api = AsyncAPI('async_api', __name__, celery_tasks={
    'map': map_task,
    'sudoku': sudoku_task
}, celery=celery, spawned=BOOST)

# Apply CORS on every blueprint
cors.init_app(sync_api)
cors.init_app(async_api)

# Register blueprints
app.register_blueprint(sync_api)
app.register_blueprint(async_api)

# Compress app
compress.init_app(app)


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({'msg': 'This resource does not exist'}), 404


if __name__ == '__main__':
    w = WSGIServer(('0.0.0.0', FLASK_SERVER_PORT), app)
    try:
        w.serve_forever()
    except KeyboardInterrupt:
        w.stop(timeout=10)
