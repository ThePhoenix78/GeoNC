from .georep import GeorepNC
from .arcgis import ArcgisNC

from pyproj import Transformer


class GeoNC(GeorepNC, ArcgisNC):
    def __init__(self):
        GeorepNC.__init__(self)
        ArcgisNC.__init__(self)
        self._to_lambert = Transformer.from_crs(3163, 4326, always_xy=True)
        self._to_epsg = Transformer.from_crs(4326, 3163, always_xy=True)

    def to_lambert(self, x, y):
        x1, y1 = self._to_lambert.transform(x, y)
        return x1, y1

    def to_epsg(self, x, y):
        x1, y1 = self._to_epsg.transform(x, y)
        return x1, y1
