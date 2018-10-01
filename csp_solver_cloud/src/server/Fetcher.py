from functools import partial

from geopy.geocoders.arcgis import ArcGIS
from geopy.geocoders.photon import Photon

from csp_solver_cloud.src.server.flask_inits import GEOCODER


class Fetcher(object):
    def __init__(self):
        self._geocoder_photon = Photon()
        self._geocoder_arcgis = ArcGIS()

        self._geocoders = {
            'PHOTON': self._photon_resolver,
            'ARCGIS': self._arcgis_resolver,
            'PHOTON|ARCGIS': partial(self._both_resolver, self._photon_resolver, self._arcgis_resolver),
            'ARCGIS|PHOTON': partial(self._both_resolver, self._arcgis_resolver, self._photon_resolver)
        }

    def _photon_resolver(self, query):
        data = self._geocoder_photon.reverse(query, language='en')

        if data:
            data = {
                'country': data.raw.get('properties').get('country').lower(),
                'key': 'admin'
            }

        return data

    def _arcgis_resolver(self, query):
        data = self._geocoder_arcgis.reverse(query)

        if data:
            data = {
                'country': data.raw.get('CountryCode').upper(),
                'key': 'adm0_a3'
            }

        return data

    def _both_resolver(self, geocoder_1, geocoder_2, query):
        return geocoder_1(query) or geocoder_2(query)

    def resolve(self, latitude, longitude):
        query = "{}, {}".format(latitude, longitude)

        # Weird error here. Two consecutives wrong countries request, it gives 404 bad request or Service TimedOut
        # In that case, you must reload the webclient page.

        # In Photon, Monaco is shown as France :(
        return self._geocoders[GEOCODER](query)
