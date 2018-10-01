import os
import warnings

from csp_solver_cloud.src.server.BaseService import BaseService

warnings.simplefilter("ignore")
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderQueryError
from csp_solver_cloud.src.server.Fetcher import Fetcher
import geopandas as gp
from csp_solver_cloud.src.map.map import Map
from csp_solver_cloud.src.server import ServiceException, ServiceCodes
import pandas as pd


class MapService(BaseService):
    def __init__(self):
        self._geo_data = gp.read_file(
            os.path.join(os.path.dirname(__file__), 'data/ne_10m_admin_1_states_provinces.shp'), encoding='utf-8')
        self._geo_data['admin'] = self._geo_data['admin'].apply(lambda x: x.lower())  # uniform criteria
        self._geolocator = Fetcher()

    def solve(self, latitude, longitude, colors):
        if latitude is None or longitude is None or colors is None:
            raise ServiceException(ServiceCodes.EMPTY_PARAMS, msg='Empty parameters')

        try:
            colors = [color for color in xrange(1, int(colors) + 1)]
        except (TypeError, ValueError) as f:
            raise ServiceException(ServiceCodes.BAD_PARAMS, msg=f.message)

        try:
            input_data = self._geolocator.resolve(latitude, longitude)
        except (GeocoderTimedOut, GeocoderServiceError, GeocoderQueryError) as e:
            raise ServiceException(ServiceCodes.FAIL, msg=e.message)

        if not input_data:
            raise ServiceException(ServiceCodes.FAIL,
                                   msg='No country found with these coordinates ({},{})'.format(latitude, longitude))

        map = Map(self._geo_data, input_data, colors, 'mrv', 'lcv')
        if map.backtracking_search():
            return self._build_json_response(map)

        return None

    def _build_json_response(self, map):
        df = pd.DataFrame.from_dict(map.variables, orient='index')
        if not df.empty:
            df.reset_index(0, inplace=True)
            df.columns = ['province', 'color']

            s_geo = map.geo_data.merge(df, left_on=map.geo_data.gn_name, right_on='province')

            return s_geo[['geometry', 'province', 'color']].to_json()

        return None
