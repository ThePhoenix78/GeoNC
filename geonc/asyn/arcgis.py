# coding : utf8
from ..utils.objects import GeoObject, GeoClass
from ..utils.georequests import GeoRequests

from urllib.parse import urlencode

# https://localisation.gouv.nc/api/openapi


class ArcgisNC(GeoRequests):
    def __init__(self):
        GeoRequests.__init__(self, "https://localisation.gouv.nc")

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

    async def get_localisation(self, number: str = "", street: str = "", limit: int = 6) -> GeoClass:
        address: str = f"{number} {street}".strip()

        s: int = len(address.split())-1 if len(address.split()) > 1 else 0

        data: dict = {
            "SingleLine": f"{address}",
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
            "maxLocations": limit,
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

    async def get_cadastre(self, number: str = "", street: str = "", limit: int = 6) -> GeoClass:
        address: str = f"{number} {street}".strip()

        s: int = len(address.split())+1 if len(address.split()) > 1 else 0

        data = {
            "SingleLine": f"{address}",
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
            "maxLocations": limit,
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
        fin = await self.arequest(method="GET", endpoint=f"/api/arcgis/rest/services/cadastre/GeocodeServer/findAddressCandidates?{data}", payload=self.payload, headers=self.headers)
        fin = fin.json

        return GeoObject(fin.get("candidates", fin))

    async def get_pois(self, number: str = "", street: str = "", limit: int = 6) -> GeoClass:
        address = f"{number} {street}".strip()

        s = len(address.split())-1 if len(address.split()) > 1 else 0
        
        data = {
            "SingleLine": f"{address}",
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
            "maxLocations": limit,
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
        fin = await self.request(method="GET", endpoint=f"/api/arcgis/rest/services/pois/GeocodeServer/findAddressCandidates?{data}", payload=self.payload, headers=self.headers)
        fin = fin.json

        return GeoObject(fin.get("candidates", fin))

    async def get_capabilities(self):
        headers: dict = {"accept": "application/json"}
        fin = await self.arequest(method="GET", endpoint=f"/api/getCapabilities", payload=self.payload, headers=headers)
        fin = fin.json

        return GeoObject(fin)        

    async def search(self, address: str, index: str = None,  limit: int = None, lat: float = None, lon: float = None, returntruegeometry: bool = None, postcode: str = None, citycode: str = None, address_type: str = None, city: str = None, category: str = None):
        address = address.strip()

        s = len(address.split())-1 if len(address.split()) > 1 else 0
        
        data: dict = {"q": address}

        if index:
            data["index"] = index

        if limit:
            data["limit"] = limit

        if lat:
            data["lat"] = lat

        if lon:
            data["lon"] = lon

        if returntruegeometry is not None:
            data["returntruegeometry"] = returntruegeometry

        if postcode:
            data["postcode"] = postcode
        
        if citycode:
            data["citycode"] = citycode
        
        if address_type:
            data["type"] = address_type

        if city:
            data["city"] = city
        
        if category:
            data["category"] = category

        data = urlencode(data).replace("%27", "%22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")

        headers: dict = {"accept": "application/json"}
        fin = await self.arequest(method="GET", endpoint=f"/api/search?{data}", payload=self.payload, headers=headers)
        fin = fin.json

        return GeoObject(fin)
    
    async def search_csv(self, filename: str, index: str = None, lat: float = None, lon: float = None, postcode: str = None, citycode: str = None, category: str = None, address_type: str = None, result_columns: list[str] = None):
        data: list[tuple[str]] = []

        if index:
            data.append(("index", index))

        if lat:
            data.append(("lat", lat))

        if lon:
            data.append(("lon", lon))

        if postcode:
            data.append(("postcode", postcode))
                         
        if citycode:
            data.append(("citycode", citycode))
        
        if address_type:
            data.append(("type", address_type))

        if category:
            data.append(("category", category))

        for result in result_columns:
            data.append(("result_columns", result))

        headers: dict = {"accept": "application/json"}

        with open(filename, "rb") as f:
            files = {"data": ("test.txt", f, "text/plain")}

            fin = await self.arequest(method="POST", endpoint=f"/api/search/csv", payload=data, headers=headers, files=files)
            fin = fin.json

        return GeoObject(fin)
    
    async def reverse(self, searchgeom: str, indexes: str = None, limit: int = None, lat: float = None, lon: float = None, returntruegeometry: bool = None, postcode: str = None, citycode: str = None, address_type: str = None, city: str = None, category: str = None):
        searchgeom = searchgeom.strip()

        s = len(searchgeom.split())-1 if len(searchgeom.split()) > 1 else 0
        
        data: dict = {"searchgeom": searchgeom}

        if indexes:
            data["indexes"] = indexes

        if limit:
            data["limit"] = limit

        if lat:
            data["lat"] = lat

        if lon:
            data["lon"] = lon

        if returntruegeometry is not None:
            data["returntruegeometry"] = returntruegeometry

        if postcode:
            data["postcode"] = postcode
        
        if citycode:
            data["citycode"] = citycode
        
        if address_type:
            data["type"] = address_type

        if city:
            data["city"] = city
        
        if category:
            data["category"] = category

        data = urlencode(data).replace("%27", "%22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")

        headers: dict = {"accept": "application/json"}
        fin = await self.arequest(method="GET", endpoint=f"/api/reverse", payload=self.payload, headers=headers)
        fin = fin.json

        return GeoObject(fin)

    async def reverse_csv(self, filename: str, indexes: str = None, lat: float = None, lon: float = None, postcode: str = None, citycode: str = None, category: str = None, address_type: str = None, result_columns: list[str] = None):
        data: list[tuple[str]] = []

        if indexes:
            data.append(("indexes", indexes))

        if lat:
            data.append(("lat", lat))

        if lon:
            data.append(("lon", lon))

        if postcode:
            data.append(("postcode", postcode))
                         
        if citycode:
            data.append(("citycode", citycode))
        
        if address_type:
            data.append(("type", address_type))

        if category:
            data.append(("category", category))

        for result in result_columns:
            data.append(("result_columns", result))

        headers: dict = {"accept": "application/json"}

        with open(filename, "rb") as f:
            files = {"data": ("test.txt", f, "text/plain")}

            fin = await self.arequest(method="POST", endpoint=f"/api/search/csv", payload=data, headers=headers, files=files)
            fin = fin.json

        return GeoObject(fin)
