# coding : utf8
from ..utils.objects import GeoObject, GeoClass
from ..utils.georequests import GeoRequests

from urllib.parse import urlencode

from io import BytesIO
from PIL import Image


# Fonds  DITTT  -  Gouvernement  de  la Nouvelle-Calédonie (2021)


class GeosgtNC(GeoRequests):
    def __init__(self):
        GeoRequests.__init__(self, "https://geosgt.gouv.nc", use_etag=False)
        self.payload = ""

    async def get_tile(self, zoom: int = 0, y: int = 0, x: int = 0, out_border: bool = False, check_out_border: bool = True):
        """
        parameters :
            zoom (int) : the zoom (3-13),
            y (int) : the y coord (epsg 3163),
            x (int) : the x coord (epsg 3163),
            outborder (bool) : get the map out of the nc
            check_outborder (bool) : return False if out of th map, else a blue square
        
        return a tile (png/jpeg)
        """
        blank = "true" if out_border else "false"
        link = f"/public/rest/services/fond_imagerie/MapServer/tile/{zoom}/{y}/{x}?blankTile={blank}"
        headers = {'cookie': "SERVERID=webadaptor2"}

        res = await self.arequest("GET", link, headers=headers)
        data = res.content

        if not check_out_border and len(data) <= 775:
            return False

        return Image.open(BytesIO(data))


class ArcGISonlineTile(GeoRequests):
    def __init__(self):
        GeoRequests.__init__(self, "https://server.arcgisonline.com", use_etag=True)
        self.payload = ""

    async def get_tile(self, zoom: int = 0, y: int = 0, x: int = 0):
        """
        parameters :
            zoom (int) : the zoom (3-13),
            y (int) : the y coord (epsg 3163),
            x (int) : the x coord (epsg 3163),
            outborder (bool) : get the map out of the nc
            check_outborder (bool) : return False if out of th map, else a blue square
        
        return a tile (png/jpeg)
        """
        link = f"/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{y}/{x}"

        res = await self.arequest("GET", link)
        data = res.content

        return Image.open(BytesIO(data))


class ArcGISTile(GeoRequests):
    def __init__(self):
        GeoRequests.__init__(self, "https://tiles.arcgis.com", use_etag=True)
        self.payload = ""
        self.headers: dict = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
            'accept': "*/*",
            'accept-language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            'accept-encoding': "json, deflate, br",
            'referer': "https://cadastre.gouv.nc/",
            'origin': "https://cadastre.gouv.nc",
            'sec-gpc': "1",
            "dnt": "1",
            'sec-fetch-dest': "empty",
            'sec-fetch-mode': "cors",
            'sec-fetch-site': "cross-site",
            "te": "trailers",
            }

    async def get_tile(self, zoom: int = 0, y: int = 0, x: int = 0):
        """
        parameters :
            zoom (int) : the zoom (3-13),
            y (int) : the y coord (epsg 3163),
            x (int) : the x coord (epsg 3163),
            outborder (bool) : get the map out of the nc
            check_outborder (bool) : return False if out of th map, else a blue square
        
        return a tile (png/jpeg)
        """
        link = f"/tiles/TZcrgU6CIbqWt9Qv/arcgis/rest/services/fond_imagerie/MapServer/tile/{zoom}/{y}/{x}"

        res = await self.arequest("GET", link)
        data = res.content

        return Image.open(BytesIO(data))