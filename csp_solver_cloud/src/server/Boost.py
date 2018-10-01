import gevent


class Boost(object):
    def __init__(self, spawned=True):
        self._spawned = spawned

    def call(self, f, *args, **kwargs):
        if self._spawned:
            return self._call_socket(f, *args, **kwargs)
        return f(*args, **kwargs)

    def _call_socket(self, f, *args, **kwargs):
        gevent.spawn(f, *args, **kwargs)
