# coding : utf8
from urllib.parse import urlencode
import http.client
import json
import gzip

# Fonds  DITTT  -  Gouvernement  de  la Nouvelle-Calédonie (2021)


class GeorepNC:
    def __init__(self, connect: bool = True):
        self.geo_conn = None
        self.tile_conn = None
        self.payload = ""

        self.image_request = "https://geosgt.gouv.nc/public/rest/services/fond_imagerie/MapServer/tile"

        self.request_header = {
            'Host': "cadastre.gouv.nc",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            'Accept': "application/json, text/plain, */*",
            'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding': "json",
            'Referer': "https://cadastre.gouv.nc/",
            'DNT': "1",
            'Connection': "keep-alive",
            'Cookie': "SERVERID=webadaptor1",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-origin"
            }

        self.coord_headers = {
            'Host': "cadastre.gouv.nc",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            'Accept': "*/*",
            'Accept-Language': "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding': "json, deflate, br",
            'Referer': "https://cadastre.gouv.nc/",
            'DNT': "1",
            'Connection': "keep-alive",
            'Cookie': "SERVERID=webadaptor1",
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-origin"
            }

        self.nic_header = {
            'Host': "cadastre.gouv.nc",
            'Connection': "keep-alive",
            'sec-ch-ua': 'Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'Accept': "application/json, text/plain, */*",
            'sec-ch-ua-mobile': "?0",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.8 Safari/537.36",
            'sec-ch-ua-platform': "Windows",
            'Sec-Fetch-Site': "same-origin",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Dest': "empty",
            'Referer': "https://cadastre.gouv.nc/",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cookie': "SERVERID=webadaptor2",
            'dnt': "1"
            }

        if connect:
            self.geo_connect()
            self.tile_connect()

    def geo_connect(self):
        """
        connect to the cadastre socket
        """
        self.geo_conn = http.client.HTTPSConnection("cadastre.gouv.nc")

    def tile_connect(self):
        """
        connect to the tile socket (png)
        """
        self.tile_conn = http.client.HTTPSConnection("geosgt.gouv.nc")

    def get_tile(self, zoom: int = 0, y: int = 0, x: int = 0, out_border: bool = False, check_out_border: bool = True):
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
        link = f"{self.image_request}/{zoom}/{y}/{x}?blankTile={blank}"
        headers = {'cookie': "SERVERID=webadaptor2"}

        self.tile_conn.request("GET", link, headers=headers)
        res = self.tile_conn.getresponse()
        data = res.read()

        if not check_out_border and len(data) <= 775:
            return False

        return data

    def get_info(self, adresse: str = ""):
        """
        return the informations related to the adresse
        """
        data = {
                "filter": {
                    "searchText": f"{adresse}",
                    "stateIds": [1]
                    }
                }
        data = urlencode(data).replace("27", "22").replace("+", "%20").replace("%20", "", 1)
        self.geo_conn.request("GET", f"/api/parcel/fts?{data}", self.payload, self.request_header)
        res = self.geo_conn.getresponse()
        fin = res.read()
        return json.loads(fin)

    def get_adresse_list(self, numero: str = "", street: str = "", nic: str = ""):
        """
        parameters :
            numero (int or str) : the numero of the adresse,
            street (str) : the street of the adresse
        return a list of dict associated with the adresse's information
            id : the id of the adresse
            num : the numero of the adresse
            street : the street's name
            nic : the nic (Numero d Inventaire Cadastral)
        """
        numero = str(numero)
        adresse = f"{numero} {street}".strip()
        if nic:
            adresse = nic.strip()
        dico = self.get_info(adresse)
        adr = street.lower().strip().split()

        if nic:
            return dico["content"]

        for values in dico["content"]:
            try:
                if adresse.lower() == values["ftsAddressLabel"].lower():
                    return values["adresses"]
                for val in values["adresses"]:
                    if numero == val["num"] and [True for i in adr if i in val["street"].lower()]:
                        return values["adresses"]
            except Exception:
                pass

    def get_from_adresse(self, numero: str = "", street: str = "", nic: str = ""):
        """
        parameters :
            numero (str) : the numero of the adresse,
            street (str) : the street of the adresse
        return a list of dict associated with the adresse's information
        """
        numero = str(numero)
        adresse = f"{numero} {street}".strip()

        if nic:
            adresse = nic.strip()

        dico = self.get_info(adresse)
        adr = street.lower().strip().split()

        if nic:
            return dico["content"]

        for values in dico["content"]:
            try:
                if adresse.lower() == values["ftsAddressLabel"].lower():
                    return values
                for val in values["adresses"]:
                    if numero == val["num"] and [True for i in adr if i in val["street"].lower()]:
                        return values
            except Exception:
                pass

    def get_from_nic(self, nic: str):
        """
        parameters :
            nic : the nic (Numero d Inventaire Cadastral)
        return a list of dict associated with the adresse's information
        """
        data = {
                "filter": {
                    "ref": f"{nic}"
                    },
                "size": 1,
                "page": 0
                }
        data = urlencode(data).replace("27", "22").replace("+", "%20").replace("%20", "", 1)
        self.geo_conn.request("GET", f"/api/parcel?{data}", self.payload, self.nic_header)
        res = self.geo_conn.getresponse()
        return json.loads(gzip.decompress(res.read()).decode())

    def get_from_coord(self, x, y):
        data = {
                "f": "json",
                "distance": "150000000000",
                "geometry": {
                    "spatialReference": {
                        "latestWkid": "3163",
                        "wkid": "3163"
                        },
                    "x": f"{x}",
                    "y": f"{y}"
                },
                "outFields": "*",
                "outSR": "3163",
                "spatialRel": "esriSpatialRelIntersects",
                "where": "1=1",
                "geometryType": "esriGeometryPoint",
                "inSR": "316"
                }

        data = urlencode(data).replace("27", "22").replace("+", "%20").replace("%20", "", 1)
        self.geo_conn.request("GET", f"/arcgisServices/cadastreV3/cadastre_consult_v3/MapServer/7/query?{data}", self.payload, self.coord_headers)
        res = self.geo_conn.getresponse()
        res = res.read()
        res = json.loads(res)
        # return res
        return {"geometryType": res["geometryType"], "spatialReference": res["spatialReference"], "features": res["features"]}
