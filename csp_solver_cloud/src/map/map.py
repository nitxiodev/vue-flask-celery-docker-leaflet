# Data source: https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/
from csp_solver_cloud.src.csp.CSP import CSP, UNASSIGNED


class Map(CSP):
    def __init__(self, geo_data, input_data, colors, variable_heuristic, domain_heuristic):
        country, key = input_data.get('country'), input_data.get('key')
        self._geo = geo_data[geo_data[key] == country][['gn_name', 'geometry']]
        self._geo['neighbors'] = self._geo['geometry'].apply(
            lambda x: self._geo[self._geo['geometry'].touches(x)].gn_name.tolist())
        self._geo.index = self._geo.gn_name
        self._data = self._geo[['neighbors']].T.to_dict(orient='list')

        map_domains = {key: colors[:] for key in self._data}
        map_variables = {key: UNASSIGNED for key in map_domains}
        map_constraints = lambda x, y: x != y

        super(Map, self).__init__(map_variables, map_domains, map_constraints,
                                  variable_heuristic, domain_heuristic)
        self.build_neighbors()

    @property
    def geo_data(self):
        return self._geo

    def solved(self):
        return all([self.variables[v] != UNASSIGNED for v in self.variables])

    def valid_assignment(self, variable, value):
        variable_neighbors = self.neighbors[variable]
        return all([self.variables[neighbor] != value for neighbor in variable_neighbors])

    def build_neighbors(self):
        for var in self.variables:
            self._neighbors[var] = set(self._data[var][0])
