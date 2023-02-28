from .georep import GeorepNC
from .arcgis import ArcgisNC
from pyproj import Transformer


class GeoNC(GeorepNC, ArcgisNC):
    def __init__(self, max: int = 6, connect: bool = True):
        GeorepNC.__init__(self, connect)
        ArcgisNC.__init__(self, max, connect)
        self._to_lambert = Transformer.from_crs(3163, 4326, always_xy=True)
        self._to_epsg = Transformer.from_crs(4326, 3163, always_xy=True)

    def to_lambert(self, x, y):
        x1, y1 = self._to_lambert.transform(x, y)
        return x1, y1

    def to_epsg(self, x, y):
        x1, y1 = self._to_epsg.transform(x, y)
        return x1, y1

    def get_coords_from_coords(self, x, y):
        return self.get_from_coord(x, y)["features"][0]["geometry"]["rings"][0]

    def get_coords_from_adresse(self, numero: str = "", street: str = ""):
        val = self.get_adresse(numero, street)[0]["attributes"]
        return self.get_from_coord(val["X"], val["Y"])["features"][0]["geometry"]["rings"][0]

    def get_coords_from_batiment(self, numero: str = "", street: str = ""):
        val = self.get_batiment(numero, street)[0]["attributes"]
        return self.get_from_coord(val["X"], val["Y"])["features"][0]["geometry"]["rings"][0]

    def get_coords_from_lieu_dit(self, numero: str = "", street: str = ""):
        val = self.get_lieu_dit(numero, street)[0]["attributes"]
        return self.get_from_coord(val["X"], val["Y"])["features"][0]["geometry"]["rings"][0]

    def get_coords_from_maritime(self, numero: str = "", street: str = ""):
        val = self.get_maritime(numero, street)[0]["attributes"]
        return self.get_from_coord(val["X"], val["Y"])["features"][0]["geometry"]["rings"][0]

    def get_coords_from_poi(self, numero: str = "", street: str = ""):
        val = self.get_poi(numero, street)[0]["attributes"]
        return self.get_from_coord(val["X"], val["Y"])["features"][0]["geometry"]["rings"][0]

    def get_coords_from_nic(self, nic: str):
        val = self.get_from_nic(nic)["content"][0]["adresses"]
        val = self.get_adresse(val[0]["num"], val[0]["street"])[0]["attributes"]
        return self.get_from_coord(val["X"], val["Y"])["features"][0]["geometry"]["rings"][0]
