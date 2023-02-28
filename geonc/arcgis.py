# coding : utf8
from urllib.parse import urlencode
import http.client
import json


class ArcgisNC:
    def __init__(self, max: int = 6, connect: bool = True):
        self.arc_conn = None
        self.payload = ""

        self.max = max

        self.headers = {
            'cookie': "SERVERID=webadaptor2",
            'Host': "geosgt-explocarto.gouv.nc",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            'Accept': "*/*",
            'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding': "json, deflate, br",
            'Referer': "https://dtsi-sgt.maps.arcgis.com/",
            'Origin': "https://dtsi-sgt.maps.arcgis.com",
            'DNT': "1",
            'Connection': "keep-alive",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "cross-site"
            }

        self.typical = {
            "spatialReference": {
                "wkid": 102100,
                "latestWkid": 3857
            },
            "candidates": []
        }

        if connect:
            self.arc_connect()

    def arc_connect(self):
        self.arc_conn = http.client.HTTPSConnection("geosgt-explocarto.gouv.nc")

    def get_all(self, numero: str = "", street: str = ""):
        res: dict = {}
        fin: dict = {}

        res["batiment"] = self.get_batiment(numero, street)
        res["adresse"] = self.get_adresse(numero, street)
        res["lieu_dit"] = self.get_lieu_dit(numero, street)
        res["maritime"] = self.get_maritime(numero, street)
        res["poi"] = self.get_poi(numero, street)

        for k, v in res.items():
            if v != self.typical and v:
                fin[k] = v

        return fin

    def get_batiment(self, numero: str = "", street: str = ""):
        adresse = f"{numero} {street}".strip()

        s = len(adresse.split())-1 if len(adresse.split()) > 1 else 0

        data = {
                "SingleLine": f"{adresse}",
                "f": "json",
                "outSR": {
                    "wkid": 102100,
                    "latestWkid": 3857
                    },
                "outFields": "*",
                "maxLocations": self.max
                }

        data = urlencode(data).replace("27", "22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        self.arc_conn.request("GET", f"/arcgis/rest/services/Geocodage/Batiment/GeocodeServer/findAddressCandidates?{data}", self.payload, self.headers)

        res = self.arc_conn.getresponse()
        fin = json.loads(res.read())
        return fin.get("candidates", fin)

    def get_adresse(self, numero: str = "", street: str = ""):
        adresse = f"{numero} {street}".strip()

        s = len(adresse.split())+1 if len(adresse.split()) > 1 else 0

        data = {
                "Single Line Input": f"{adresse}",
                "f": "json",
                "outSR": {
                    "wkid": 102100,
                    "latestWkid": 3857
                    },
                "outFields": "*",
                "maxLocations": self.max
                }

        data = urlencode(data).replace("27", "22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        self.arc_conn.request("GET", f"/arcgis/rest/services/Geocodage/Adresse/GeocodeServer/findAddressCandidates?{data}", self.payload, self.headers)

        res = self.arc_conn.getresponse()
        fin = json.loads(res.read())
        return fin.get("candidates", fin)

    def get_lieu_dit(self, numero: str = "", street: str = ""):
        adresse = f"{numero} {street}".strip()

        s = len(adresse.split())-1 if len(adresse.split()) > 1 else 0

        data = {
                "SingleLine": f"{adresse}",
                "f": "json",
                "outSR": {
                    "wkid": 102100,
                    "latestWkid": 3857
                    },
                "outFields": "*",
                "maxLocations": self.max
                }

        data = urlencode(data).replace("27", "22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        self.arc_conn.request("GET", f"/arcgis/rest/services/Geocodage/Lieu_dit/GeocodeServer/findAddressCandidates?{data}", self.payload, self.headers)

        res = self.arc_conn.getresponse()
        fin = json.loads(res.read())
        return fin.get("candidates", fin)

    def get_maritime(self, numero: str = "", street: str = ""):
        adresse = f"{numero} {street}".strip()

        s = len(adresse.split())-1 if len(adresse.split()) > 1 else 0

        data = {
                "SingleLine": f"{adresse}",
                "f": "json",
                "outSR": {
                    "wkid": 102100,
                    "latestWkid": 3857
                    },
                "outFields": "*",
                "maxLocations": self.max
                }

        data = urlencode(data).replace("27", "22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        self.arc_conn.request("GET", f"/arcgis/rest/services/Geocodage/maritime/GeocodeServer/findAddressCandidates?{data}", self.payload, self.headers)

        res = self.arc_conn.getresponse()
        fin = json.loads(res.read())
        return fin.get("candidates", fin)

    def get_poi(self, numero: str = "", street: str = ""):
        adresse = f"{numero} {street}".strip()

        s = len(adresse.split())-1 if len(adresse.split()) > 1 else 0

        data = {
                "SingleLine": f"{adresse}",
                "f": "json",
                "outSR": {
                    "wkid": 102100,
                    "latestWkid": 3857
                    },
                "outFields": "*",
                "maxLocations": self.max
                }

        data = urlencode(data).replace("27", "22").replace("+", "%20", s).replace("%2A", "*").replace("+", "")
        self.arc_conn.request("GET", f"/arcgis/rest/services/Geocodage/Poi/GeocodeServer/findAddressCandidates?{data}", self.payload, self.headers)

        res = self.arc_conn.getresponse()
        fin = json.loads(res.read())
        return fin.get("candidates", fin)
