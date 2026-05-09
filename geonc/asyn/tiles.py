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