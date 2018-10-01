# Configurations for flask-celery-socketio
class Baseconfig(object):
    DEBUG = False
    TESTING = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_IGNORE_RESULT = False
    CELERY_ROUTES = {
        'csp_solver_cloud.src.server.maptask': {'queue': 'long_running'},
        'csp_solver_cloud.src.server.sudokutask': {'queue': 'short_running'}
    }
    CELERYD_PREFETCH_MULTIPLIER = 64
    CELERY_MESSAGE_COMPRESSION = 'gzip'
    CELERY_TASK_RESULT_EXPIRES = 3600  # 1 hour
    SOCKETIO_BROKER_URL = 'redis://localhost:6379/0'


class ProductionConfig(Baseconfig):
    CELERY_TASK_RESULT_EXPIRES = 600  # 10 minutes
    CELERY_BROKER_URL = 'redis://redis/0'
    CELERY_RESULT_BACKEND = 'redis://redis/0'
    SOCKETIO_BROKER_URL = 'redis://redis/0'


class DevConfig(Baseconfig):
    DEBUG = True


class TestConfig(Baseconfig):
    TESTING = True
    SOCKETIO_BROKER_URL = None
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
