## Run with[.../numbers_solver/tests/$]: nosetests --with-coverage --cover-package=.. __init__.py
import json
import unittest

import geopandas as gp
from celery.exceptions import Reject
from geopy.exc import GeocoderTimedOut
from hamcrest import assert_that, equal_to, is_, instance_of, empty, calling, raises
from kombu.exceptions import OperationalError
from mock import mock, PropertyMock

import csp_solver_cloud.src.server.Fetcher as inits
from csp_solver_cloud.src.server import ServiceCodes, ServiceException
from csp_solver_cloud.src.server.Boost import Boost
from csp_solver_cloud.src.server.Fetcher import Fetcher
from csp_solver_cloud.src.server.MapService import MapService
from csp_solver_cloud.src.server.SudokuService import SudokuService
from csp_solver_cloud.src.server.flask_inits import createApp, celery
from csp_solver_cloud.src.server.flask_server import app
from csp_solver_cloud.src.server.flask_socketio_server import socketio
from csp_solver_cloud.src.server.maptask import MapTask
from csp_solver_cloud.src.server.sudokutask import SudokuTask


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class testFetcher(unittest.TestCase):
    def setUp(self):
        self._data = AttrDict()

    @mock.patch('csp_solver_cloud.src.server.Fetcher.Photon.reverse', autospec=True)
    def testResolveWithPhoton(self, mock_photon):
        self._data['raw'] = {
            'properties': {
                'country': 'spain'
            }
        }
        mock_photon.return_value = self._data
        inits.GEOCODER = 'photon'.upper()
        _fetcher = Fetcher()

        ret = _fetcher.resolve(1, 1)
        assert_that(ret, equal_to({'country': 'spain', 'key': 'admin'}))

        del self._data['raw']

    @mock.patch('csp_solver_cloud.src.server.Fetcher.ArcGIS.reverse', autospec=True)
    def testResolveWithArcgis(self, mock_photon):
        self._data['raw'] = {
            'CountryCode': 'ESP'
        }
        mock_photon.return_value = self._data
        inits.GEOCODER = 'arcgis'.upper()
        _fetcher = Fetcher()

        ret = _fetcher.resolve(1, 1)
        assert_that(ret, equal_to({'country': 'ESP', 'key': 'adm0_a3'}))

        del self._data['raw']

    @mock.patch('csp_solver_cloud.src.server.Fetcher.ArcGIS.reverse', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.Fetcher.Photon.reverse', autospec=True)
    def testResolveWithArcgisPhoton(self, mock_photon, mock_argis):
        # Argis will fail and we retrieve data from photon geocoder
        mock_argis.return_value = None

        self._data['raw'] = {
            'properties': {
                'country': 'spain'
            }
        }
        mock_photon.return_value = self._data
        inits.GEOCODER = 'arcgis|photon'.upper()
        _fetcher = Fetcher()

        ret = _fetcher.resolve(1, 1)
        assert_that(ret, equal_to({'country': 'spain', 'key': 'admin'}))

        del self._data['raw']

    @mock.patch('csp_solver_cloud.src.server.Fetcher.ArcGIS.reverse', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.Fetcher.Photon.reverse', autospec=True)
    def testResolveWithPhotonArcgis(self, mock_photon, mock_argis):
        # Photon will fail and we retrieve data from arcgis geocoder
        mock_photon.return_value = None

        self._data['raw'] = {
            'CountryCode': 'ESP'
        }
        mock_argis.return_value = self._data
        inits.GEOCODER = 'arcgis|photon'.upper()
        _fetcher = Fetcher()

        ret = _fetcher.resolve(1, 1)
        assert_that(ret, equal_to({'country': 'ESP', 'key': 'adm0_a3'}))

        del self._data['raw']

    def testResolveWithNoValidGeocoder(self):
        inits.GEOCODER = 'no_exists'.upper()
        _fetcher = Fetcher()
        assert_that(calling(_fetcher.resolve).with_args(1, 1), raises(KeyError))


class testBoost(unittest.TestCase):
    def setUp(self):
        self._function = lambda x: x + 2

    def testNormalTask(self):
        _boost = Boost(spawned=False)
        ret = _boost.call(self._function, 0)

        assert_that(ret, equal_to(2))

    @mock.patch('csp_solver_cloud.src.server.Boost.gevent.spawn', autospec=True)
    def testGeventTask(self, mock_class):
        _boost = Boost(spawned=True)
        mock_class.return_value = None
        ret = _boost.call(self._function, 0)

        assert_that(ret, is_(None))


class testSudokuTask(unittest.TestCase):
    def setUp(self):
        with mock.patch('csp_solver_cloud.src.server.sudokutask.SudokuService.__init__') as m:
            m.return_value = None
            celery.config_from_object('csp_solver_cloud.src.server.config.TestConfig')
            self._celery_task = SudokuTask()

    def tearDown(self):
        celery.close()

    @mock.patch('csp_solver_cloud.src.server.sudokutask.SudokuService.solve', autospec=True)
    def testRun(self, mock_class):
        with mock.patch('csp_solver_cloud.src.server.sudokutask.SudokuTask.update_state'):
            mock_class.return_value = []
            recv = self._celery_task.run('011110325998440', 1, None)

            assert_that(recv, equal_to({'solution': []}))

    @mock.patch('csp_solver_cloud.src.server.sudokutask.SudokuService.solve', autospec=True)
    def testRunException(self, mock_class):
        with mock.patch('csp_solver_cloud.src.server.sudokutask.SudokuTask.update_state'):
            mock_class.side_effect = ServiceException(ServiceCodes.FAIL, msg='')
            assert_that(calling(self._celery_task.run).with_args('011110325998440', 1, None), raises(Reject))


class testMapTask(unittest.TestCase):
    def setUp(self):
        with mock.patch('csp_solver_cloud.src.server.maptask.MapService.__init__') as m:
            m.return_value = None
            celery.config_from_object('csp_solver_cloud.src.server.config.TestConfig')
            self._celery_task = MapTask()

    def tearDown(self):
        celery.close()

    @mock.patch('csp_solver_cloud.src.server.maptask.MapService.solve', autospec=True)
    def testRun(self, mock_class):
        with mock.patch('csp_solver_cloud.src.server.maptask.MapTask.update_state'):
            mock_class.return_value = []
            recv = self._celery_task.run(100, 51, 1, 1, None)

            assert_that(recv, equal_to({'solution': []}))

    @mock.patch('csp_solver_cloud.src.server.maptask.MapService.solve', autospec=True)
    def testRunException(self, mock_class):
        with mock.patch('csp_solver_cloud.src.server.maptask.MapTask.update_state'):
            mock_class.side_effect = ServiceException(ServiceCodes.FAIL, msg='')
            assert_that(calling(self._celery_task.run).with_args(1, 1, 4, 1, None), raises(Reject))


class testFlaskServer(unittest.TestCase):
    def setUp(self):
        app.config.from_object('csp_solver_cloud.src.server.config.TestConfig')
        celery.config_from_object('csp_solver_cloud.src.server.config.TestConfig')
        self._return_task = AttrDict()
        self._flask_app = app.test_client()

    def testApiNotFound(self):
        recv = self._flask_app.post('/not_found')
        assert_that(recv.status_code, equal_to(404))

    def testMapSyncApiNoData(self):
        recv = self._flask_app.post('/map_sync')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('Data must be encoded in a JSON object!'))

    def testSudokuSyncApiNoData(self):
        recv = self._flask_app.post('/sudoku_sync')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('Data must be encoded in a JSON object!'))

    @mock.patch('csp_solver_cloud.src.server.sync_api.MapService.solve', autospec=True)
    def testMapSyncDatawithEmptyParams(self, mock_class):
        mock_class.side_effect = ServiceException(ServiceCodes.EMPTY_PARAMS, msg='')
        recv = self._flask_app.post('/map_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(422))

    @mock.patch('csp_solver_cloud.src.server.sync_api.SudokuService.solve', autospec=True)
    def testSudokuSyncDatawithEmptyParams(self, mock_class):
        mock_class.side_effect = ServiceException(ServiceCodes.EMPTY_PARAMS, msg='')
        recv = self._flask_app.post('/sudoku_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(422))

    @mock.patch('csp_solver_cloud.src.server.sync_api.MapService.solve', autospec=True)
    def testMapSyncDataFail(self, mock_class):
        mock_class.side_effect = ServiceException(ServiceCodes.FAIL, msg='')
        recv = self._flask_app.post('/map_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(409))

    @mock.patch('csp_solver_cloud.src.server.sync_api.SudokuService.solve', autospec=True)
    def testSudokuSyncDataFail(self, mock_class):
        mock_class.side_effect = ServiceException(ServiceCodes.FAIL, msg='')
        recv = self._flask_app.post('/sudoku_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(409))

    @mock.patch('csp_solver_cloud.src.server.sync_api.MapService.solve', autospec=True)
    def testMapSyncDataOk(self, mock_class):
        mock_class.return_value = "ok"
        recv = self._flask_app.post('/map_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(200))
        assert_that(eval(recv.data), equal_to({'solution': "ok"}))

    @mock.patch('csp_solver_cloud.src.server.sync_api.SudokuService.solve', autospec=True)
    def testSudokuSyncDataOk(self, mock_class):
        mock_class.return_value = "ok"
        recv = self._flask_app.post('/sudoku_sync', data=json.dumps(dict(foo='1')), content_type='application/json')

        assert_that(recv.status_code, equal_to(200))
        assert_that(eval(recv.data), equal_to({'solution': "ok"}))

    def testMapAsyncApiNoData(self):
        recv = self._flask_app.post('/map_async')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('Data must be encoded in a JSON object!'))

    def testSudokuAsyncApiNoData(self):
        recv = self._flask_app.post('/sudoku_async')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('Data must be encoded in a JSON object!'))

    def testMapAsyncApiNoId(self):
        recv = self._flask_app.post('/map_async', data=json.dumps(dict(lat='1', long='2', colors='3')),
                                    content_type='application/json')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('In async mode, client uuid is mandatory'))

    def testSudokuAsyncApiNoId(self):
        recv = self._flask_app.post('/sudoku_async', data=json.dumps(dict(foo='1')), content_type='application/json')
        assert_that(recv.status_code, equal_to(422))
        assert_that(eval(recv.data), equal_to('In async mode, client uuid is mandatory'))

    @mock.patch('csp_solver_cloud.src.server.async_api.Boost.call', autospec=True)
    # @mock.patch('csp_solver_cloud.src.server.flask_server.MapTask.delay', autospec=True)
    def testMapAsyncDatawithEmptyParams(self, mock_class):  # Simulates not spawned call
        mock_class.side_effect = OperationalError
        recv = self._flask_app.post('/map_async', data=json.dumps(dict(lat='1', long='2', colors='3', id='1')),
                                    content_type='application/json')

        assert_that(recv.status_code, equal_to(503))

    @mock.patch('csp_solver_cloud.src.server.async_api.Boost.call', autospec=True)
    # @mock.patch('csp_solver_cloud.src.server.flask_server.MapTask.delay', autospec=True)
    def testMapAsyncDataBadTaskResult(self, mock_class):  # Simulates spawned call
        mock_class.return_value = None
        recv = self._flask_app.post('/map_async', data=json.dumps(dict(lat='1', long='2', colors='3', id='1')),
                                    content_type='application/json')

        assert_that(recv.status_code, equal_to(201))

    @mock.patch('csp_solver_cloud.src.server.async_api.Boost.call', autospec=True)
    # @mock.patch('csp_solver_cloud.src.server.flask_server.MapTask.delay', autospec=True)
    def testMapAsyncDataOk(self, mock_class):  # Simulates spawned call
        self._return_task['id'] = 1234
        mock_class.return_value = self._return_task
        recv = self._flask_app.post('/map_async', data=json.dumps(dict(lat='1', long='2', colors='3', id='1')),
                                    content_type='application/json')

        assert_that(recv.status_code, equal_to(201))
        assert_that(eval(recv.data), equal_to('1234'))
        del self._return_task['id']

    @mock.patch('csp_solver_cloud.src.server.async_api.Boost.call', autospec=True)
    def testSudokuAsyncDatawithEmptyParams(self, mock_class):
        mock_class.side_effect = OperationalError
        recv = self._flask_app.post('/sudoku_async', data=json.dumps(dict(foo='1', id='1')),
                                    content_type='application/json')

        assert_that(recv.status_code, equal_to(503))

    @mock.patch('csp_solver_cloud.src.server.async_api.Boost.call', autospec=True)
    def testSudokuAsyncBadTaskResult(self, mock_class):
        mock_class.return_value = None
        recv = self._flask_app.post('/sudoku_async', data=json.dumps(dict(foo='1', id='1')),
                                    content_type='application/json')

        assert_that(recv.status_code, equal_to(201))

    @mock.patch('csp_solver_cloud.src.server.async_api.Boost.call', autospec=True)
    def testSudokuAsyncOk(self, mock_class):
        self._return_task['id'] = 1234
        mock_class.return_value = self._return_task
        recv = self._flask_app.post('/sudoku_async', data=json.dumps(dict(foo='1', id='1')),
                                    content_type='application/json')

        assert_that(recv.status_code, equal_to(201))
        assert_that(eval(recv.data), equal_to('1234'))
        del self._return_task['id']

    @mock.patch('csp_solver_cloud.src.server.flask_server.celery.AsyncResult', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['result'] = 444
        self._return_task['state'] = 'PENDING'
        mock_class.return_value = self._return_task
        recv = self._flask_app.get('/progress/1')

        assert_that(recv.status_code, equal_to(404))
        assert_that(eval(recv.data)['status'], equal_to('PENDING'))

        del self._return_task['result']
        del self._return_task['state']

    @mock.patch('csp_solver_cloud.src.server.flask_server.celery.AsyncResult', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['result'] = [0, 1]
        self._return_task['state'] = 'FAILURE'
        mock_class.return_value = self._return_task
        recv = self._flask_app.get('/progress/1')

        assert_that(recv.status_code, equal_to(400))
        assert_that(eval(recv.data)['status'], equal_to('FAILURE'))

        del self._return_task['result']
        del self._return_task['state']

    @mock.patch('csp_solver_cloud.src.server.flask_server.celery.AsyncResult', autospec=True)
    def testAsyncDataOk(self, mock_class):
        self._return_task['result'] = {'solution': []}
        self._return_task['state'] = 'SUCCESS'
        mock_class.return_value = self._return_task
        recv = self._flask_app.get('/progress/1')

        assert_that(recv.status_code, equal_to(200))
        assert_that(eval(recv.data)['status'], equal_to('SUCCESS'))

        del self._return_task['result']
        del self._return_task['state']


class testSocketIOServer(unittest.TestCase):
    def setUp(self):
        self._flask_app = createApp('csp_solver_cloud.src.server.config.TestConfig', socket_io=True)
        self.app = socketio.test_client(self._flask_app)

    def testMyId(self):
        self.app.emit('my_id')
        recv = self.app.get_received()

        assert_that(recv[0]['args'][0], instance_of(str))
        assert_that(recv[0]['name'], equal_to('connected'))

    def testConnect(self):
        self.app.connect()
        recv = self.app.get_received()
        assert_that(recv, empty())

    def testDisconnect(self):
        self.app.disconnect()
        recv = self.app.get_received()
        assert_that(recv, empty())


class testMapService(unittest.TestCase):
    def setUp(self):
        with mock.patch('csp_solver_cloud.src.server.MapService.gp') as mockk:
            mockk.read_file.return_value = gp.GeoDataFrame(['a'], columns=['admin'])
            self._service = MapService()

    def testEmptyParameters(self):
        try:
            self._service.solve(None, None, None)
        except ServiceException as f:
            assert_that(f.errorcode, equal_to(ServiceCodes.EMPTY_PARAMS))

    def testBadInput(self):
        try:
            self._service.solve(1, 2, [])
        except ServiceException as f:
            assert_that(f.errorcode, equal_to(ServiceCodes.BAD_PARAMS))

    @mock.patch('csp_solver_cloud.src.server.MapService.Fetcher.resolve', autospec=True)
    def testBadReverseGeocoding(self, mock_resolve):
        try:
            mock_resolve.side_effect = GeocoderTimedOut
            self._service.solve(1, 2, 3)
        except ServiceException as f:
            assert_that(f.errorcode, equal_to(ServiceCodes.FAIL))

    @mock.patch('csp_solver_cloud.src.server.MapService.Fetcher.resolve', autospec=True)
    def testNotInputDataonReverseGeocoding(self, mock_resolve):
        try:
            mock_resolve.return_value = None
            self._service.solve(1, 2, 1)
        except ServiceException as f:
            assert_that(f.errorcode, equal_to(ServiceCodes.FAIL))

    @mock.patch('csp_solver_cloud.src.server.MapService.Map.backtracking_search', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.MapService.Map.__init__', autospec=True)
    def testSudokuwithNoSolution(self, mock_sudoku, mock_back):
        with mock.patch('csp_solver_cloud.src.server.MapService.Fetcher.resolve') as mokk:
            mokk.return_value = 1
            mock_sudoku.return_value = None
            mock_back.return_value = False
            solution = self._service.solve(1, 1, 1)
            assert_that(solution, is_(None))

    @mock.patch('csp_solver_cloud.src.server.MapService.MapService._build_json_response', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.MapService.Map.backtracking_search', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.MapService.Map.__init__', autospec=True)
    def testSudokuwithNoSolution(self, mock_sudoku, mock_back, mock_response):
        with mock.patch('csp_solver_cloud.src.server.MapService.Fetcher.resolve') as mokk:
            mokk.return_value = 1
            mock_sudoku.return_value = None
            mock_back.return_value = True
            mock_response.return_value = "OK!"
            solution = self._service.solve(1, 1, 1)
            assert_that(solution, equal_to("OK!"))


class testSudokuService(unittest.TestCase):
    def setUp(self):
        self._service = SudokuService()

    def testEmptyParameters(self):
        try:
            self._service.solve(None)
        except ServiceException as f:
            assert_that(f.errorcode, equal_to(ServiceCodes.EMPTY_PARAMS))

    def testBadInput(self):
        try:
            self._service.solve("")
        except ServiceException as f:
            assert_that(f.errorcode, equal_to(ServiceCodes.BAD_PARAMS))

    @mock.patch('csp_solver_cloud.src.server.SudokuService.Sudoku.backtracking_search', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.SudokuService.Sudoku.__init__', autospec=True)
    def testSudokuwithNoSolution(self, mock_sudoku, mock_back):
        mock_sudoku.return_value = None
        mock_back.return_value = False
        solution = self._service.solve("0" * 81)
        assert_that(solution, is_(None))

    @mock.patch('csp_solver_cloud.src.server.SudokuService.Sudoku.variables', new_callable=PropertyMock)
    @mock.patch('csp_solver_cloud.src.server.SudokuService.Sudoku.backtracking_search', autospec=True)
    @mock.patch('csp_solver_cloud.src.server.SudokuService.Sudoku.__init__', autospec=True)
    def testSudokuwithSolution(self, mock_sudoku, mock_back, mock_variables):
        mock_sudoku.return_value = None
        mock_back.return_value = True
        mock_variables.return_value = {0: "No", 1: "solution"}
        solution = self._service.solve("0" * 81)
        assert_that(solution, equal_to("Nosolution"))
