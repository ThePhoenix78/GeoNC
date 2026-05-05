# coding : utf8
from ..utils.objects import GeoObject, GeoClass
from ..utils.georequests import GeoRequests

from urllib.parse import urlencode
import http.client


# Fonds  DITTT  -  Gouvernement  de  la Nouvelle-Calédonie (2021)


class GeorepNC(GeoRequests):
    def __init__(self):
        GeoRequests.__init__(self, "https://cadastre.gouv.nc")
        self.tile_conn = None
        self.payload = ""

        self.image_request = "https://geosgt.gouv.nc/public/rest/services/fond_imagerie/MapServer/tile"

        self.request_header = {
            'Host': "cadastre.gouv.nc",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
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
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
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
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.4692.8 Safari/537.36",
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

    def get_info(self, adresse: str = "") -> GeoClass:
        """
        return the informations related to the adresse
        """
        data = {
                "filter": {
                    "searchText": f"{adresse}",
                    "stateIds": [1]
                    }
                }
        data = urlencode(data).replace("%27", "%22").replace("+", "%20").replace("%20", "", 1)
        fin = self.request(method="GET", endpoint=f"/api/parcel/fts?{data}", payload=self.payload, headers=self.request_header)
        fin = fin.json
        
        return GeoObject(fin)

    def get_adresse_list(self, number: str = "", street: str = "", nic: str = "") -> list[GeoClass]:
        """
        parameters :
            number (int or str) : the number of the adresse,
            street (str) : the street of the adresse
        
        return a list of GeoClass associated with the adresse's information
            id : the id of the adresse
            num : the number of the adresse
            street : the street's name
            nic : the nic (numero d'Inventaire Cadastral)
        """
        number = str(number)
        adresse = f"{number} {street}".strip()
        
        if nic:
            adresse = nic.strip()
        
        dico: GeoClass = self.get_info(adresse)
        adr = street.lower().strip().split()

        if nic:
            return dico.content

        for value in dico.content:
            try:
                if adresse.lower() == value.ftsAddressLabel.lower():
                    return value.adresses
            
                for val in value.adresses:
                    if number == val.num and [True for i in adr if i in val.street.lower()]:
                        return value.adresses
            
            except Exception:
                pass

    def get_adresse(self, number: str = "", street: str = "", nic: str = "") -> list[GeoClass]:
        """
        parameters :
            number (str) : the number of the adresse,
            street (str) : the street of the adresse

        return a list of dict associated with the adresse's information
        """
        number = str(number)
        adresse = f"{number} {street}".strip()

        if nic:
            adresse = nic.strip()

        dico: GeoClass = self.get_info(adresse)
        adr = street.lower().strip().split()

        if nic:
            return dico.content

        for value in dico.content:
            try:
                if adresse.lower() == value.ftsAddressLabel.lower():
                    return value
                
                for val in value.adresses:
                    if number == val.num and [True for i in adr if i in val.street.lower()]:
                        return value
            
            except Exception:
                pass

    def get_nic(self, nic: str) -> list[GeoClass]:
        """
        parameters :
            nic : the nic (numero d'Inventaire Cadastral)

        return a list of GeoClass associated with the adresse's information
        """
        data = {
            "filter": {
                "ref": f"{nic}"
                },
            "size": 1,
            "page": 0
        }

        data = urlencode(data).replace("%27", "%22").replace("+", "%20").replace("%20", "", 1)
        res = self.request(method="GET", endpoint=f"/api/parcel?{data}", payload=self.payload, headers=self.nic_header)
        res = res.json

        return GeoObject(res)

    def get_coords(self, x: float = None, y: float = None, nic: str = None) -> GeoClass:
        if x and y:
            data: dict = {
                "f": "json",
                "distance": "150000000000",
                "geometry": {
                    "x": f"{x}",
                    "y": f"{y}"
                },
                "outFields": "*",
                "outSR": "102100",
                "spatialRel": "esriSpatialRelIntersects",
                "where": "1=1",
                "geometryType": "esriGeometryPoint",
                "inSR": "102100"
            }

            data = urlencode(data).replace("%27", "%22").replace("+", "%20").replace("%20", "", 1)
        
        elif nic:
            data: dict = {
                "f": "json",
                "outSR": "102100",
                "spatialRel": "esriSpatialRelIntersects",
                "where": f"nic_graphique='{nic}'"
            }

            data = urlencode(data).replace("+", "%20").replace("%20", "", 1)

        res = self.request(method="GET", endpoint=f"/arcgisServices/cadastreV3/cadastre_consult_v333/MapServer/7/query?{data}", payload=self.payload, headers=self.coord_headers)
        res = res.json
        
        return GeoObject({"geometryType": res["geometryType"], "spatialReference": res["spatialReference"], "features": res["features"]})
