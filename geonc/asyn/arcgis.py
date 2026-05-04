# coding : utf8
from ..utils.objects import GeoObject, GeoClass
from ..utils.georequests import GeoRequests

from urllib.parse import urlencode



class ArcgisNC(GeoRequests):
    def __init__(self, max_results: int = 6):
        GeoRequests.__init__(self, "https://localisation.gouv.nc")

        self.max_results: int = max_results

        self.payload: str = ""
        self.headers: dict = {
            'Host': "localisation.gouv.nc",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
            'Accept': "*/*",
            'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding': "json, deflate, br",
            'Referer': "https://dtsi-sgt.maps.arcgis.com/",
            'Origin': "https://dtsi-sgt.maps.arcgis.com",
            'Sec-GPC': "1",
            'Connection': "keep-alive",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "cross-site",
            "Priority": "u=0",
            }

        self.typical = {
            "spatialReference": {
                "wkid": 102100,
                "latestWkid": 3857
            },
            "candidates": []
        }

    async def get_all(self, number: str = "", street: str = "") -> GeoClass:
        res: dict = {}
        fin: dict = {}

        res["localisation"] = await self.get_localisation(number, street)
        res["cadastre"] = await self.get_cadastre(number, street)
        res["poi"] = await self.get_pois(number, street)

        for k, v in res.items():
            if v != self.typical and v:
                fin[k] = v

        return GeoObject(fin)

    async def get_localisation(self, number: str = "", street: str = "") -> GeoClass:
        adresse: str = f"{number} {street}".strip()

        s: int = len(adresse.split())-1 if len(adresse.split()) > 1 else 0

        data: dict = {
            "SingleLine": f"{adresse}",
            "location": {
                "spatialReference": {
                    "latestWkid":3857,
                    "wkid":102100,
                    "falseM":-100000,
                    "falseX":-20037700,
                    "falseY":-30241100,
                    "falseZ":-100000,
                    "mTolerance":0.001,
                    "mUnits":10000,
                    "xyTolerance":0.001,
                    "xyUnits":10000,
                    "zTolerance":0.001,
                    "zUnits":10000
                },
                "x":18533232.873921447,
                "y":-2536034.3563922304
            },
            "maxLocations": self.max_results,
            "outSR": {
                "latestWkid":3857,
                "wkid":102100,
                "falseM":-100000,
                "falseX":-20037700,
                "falseY":-30241100,
                "falseZ":-100000,
                "mTolerance":0.001,
                "mUnits":10000,
                "xyTolerance":0.001,
                "xyUnits":10000,
                "zTolerance":0.001,
                "zUnits":10000
            },
            "f": "json",
        }

        data: bytes = urlencode(data).replace("%27", "%22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")

        fin = await self.arequest(method="GET", endpoint=f"/api/arcgis/rest/services/localisations/GeocodeServer/findAddressCandidates?{data}", payload=self.payload, headers=self.headers)
        fin = fin.json
        
        return GeoObject(fin.get("candidates", fin))

    async def get_cadastre(self, number: str = "", street: str = "") -> GeoClass:
        adresse: str = f"{number} {street}".strip()

        s: int = len(adresse.split())+1 if len(adresse.split()) > 1 else 0

        data = {
            "SingleLine": f"{adresse}",
            "location": {
                "spatialReference": {
                    "latestWkid":3857,
                    "wkid":102100,
                    "falseM":-100000,
                    "falseX":-20037700,
                    "falseY":-30241100,
                    "falseZ":-100000,
                    "mTolerance":0.001,
                    "mUnits":10000,
                    "xyTolerance":0.001,
                    "xyUnits":10000,
                    "zTolerance":0.001,
                    "zUnits":10000
                },
                "x":18533232.873921447,
                "y":-2536034.3563922304
            },
            "maxLocations": self.max_results,
            "outSR": {
                "latestWkid":3857,
                "wkid":102100,
                "falseM":-100000,
                "falseX":-20037700,
                "falseY":-30241100,
                "falseZ":-100000,
                "mTolerance":0.001,
                "mUnits":10000,
                "xyTolerance":0.001,
                "xyUnits":10000,
                "zTolerance":0.001,
                "zUnits":10000
            },
            "f": "json",
        }

        data: bytes = urlencode(data).replace("%27", "%22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        
        fin = await self.request(method="GET", endpoint=f"/api/arcgis/rest/services/cadastre/GeocodeServer/findAddressCandidates?{data}", payload=self.payload, headers=self.headers)
        fin = fin.json

        return GeoObject(fin.get("candidates", fin))

    async def get_pois(self, number: str = "", street: str = "") -> GeoClass:
        adresse = f"{number} {street}".strip()

        s = len(adresse.split())-1 if len(adresse.split()) > 1 else 0
        
        data = {
            "SingleLine": f"{adresse}",
            "location": {
                "spatialReference": {
                    "latestWkid":3857,
                    "wkid":102100,
                    "falseM":-100000,
                    "falseX":-20037700,
                    "falseY":-30241100,
                    "falseZ":-100000,
                    "mTolerance":0.001,
                    "mUnits":10000,
                    "xyTolerance":0.001,
                    "xyUnits":10000,
                    "zTolerance":0.001,
                    "zUnits":10000
                },
                "x":18533232.873921447,
                "y":-2536034.3563922304
            },
            "maxLocations": self.max_results,
            "outSR": {
                "latestWkid":3857,
                "wkid":102100,
                "falseM":-100000,
                "falseX":-20037700,
                "falseY":-30241100,
                "falseZ":-100000,
                "mTolerance":0.001,
                "mUnits":10000,
                "xyTolerance":0.001,
                "xyUnits":10000,
                "zTolerance":0.001,
                "zUnits":10000
            },
            "f": "json",
        }

        data = urlencode(data).replace("%27", "%22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        
        fin = await self.arequest(method="GET", endpoint=f"/api/arcgis/rest/services/pois/GeocodeServer/findAddressCandidates?{data}", payload=self.payload, headers=self.headers)
        fin = fin.json

        return GeoObject(fin.get("candidates", fin))
