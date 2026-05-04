# GeoNC


### utilisation de l'API

* ##### GeorepNC

* ##### ArcgisNC

* ##### GeoNC


## GeorepNC

### Paramètres

* __geo_conn__ : la connection avec le serveur
* __payload__ : infos pour les requetes (ne pas toucher)
* __request_header__ : header des requetes liées aux demandes vers le serveur
* __coord_headers__ : header des requetes liées aux coordonées
* __nic_header__ : header des requetes liées au NIC


### Méthodes
* __get_info__ _(adresse : str)_ : permet de retourner des infos liées a l'adresse

* __get_adresse_list__ _(numero: str="", street: str="", nic: str="")_ : permet de retourner une liste d'adresse correspondant a la requete

* __get_adresse__ _(numero: str="", street: str="", nic="")_ : retourne les informations complètes liées a l'adresse / nic

* __get_nic__ _(nic: str)_ : retourne les informations relative au nic

* __get_coord__ _(x, y)_ : retourne les informations correspondant aux coordonnées


## ArcgisNC

### Arguments

* __max__ : int = 6 , le nombre maximum d'éléments dans la réponse
* __connect__ : bool = True

### Paramètres

* __arc_conn__ : la connection avec le serveur
* __payload__ : infos pour les requetes (ne pas toucher)
* __headers__ : header des requetes liées aux demandes vers le serveur
* __typical__ : données comprise dans les réponses vides

### Méthodes
* __arc_connect__ : permet de lier le client au serveur (automatique)

* __get_adresse__ _(numero: str="", street: str="")_ : permet de retourner une liste d'adresses correspondant a la requete

* __get_maritime__ _(numero: str="", street: str="")_ : permet de retourner une liste d'espaces maritime correspondant a la requete

* __get_pois__ _(numero: str="", street: str="")_ : permet de retourner une liste de POI correspondant a la requete

* __get_all__ _(numero: str = "", street: str = "")_ : retourne le résultat (si il existe) de toute les requetes au dessus

## GeoNC

### Une combinaison de GeorepNC et ArcgisNC

### Arguments

* __max_results__ : int = 6 , le nombre maximum d'éléments dans la réponse
* __connect__ : bool = True

### Paramètres

* __\_to_lambert__ : classe pour transformer du espg (nc) en lambert (universel) (ne pas toucher)
* __\_to_epsg__ : classe pour transformer du lambert (universel) en espg (nc) (ne pas toucher)


### Exemple de code
```py
from geonc.sync import GeoNC
# from geonc.asyn import GeoNC

client = GeoNC()

val1 = client.get_adresse(street="Jean Jaures")
val2 = client.get_nic("xxxxx-xxxx")
val3 = client.get_coord(10, 20)

```

Mention légales georep : https://cadastre.gouv.nc/a-propos

Mention légales arcgis : https://georep-dtsi-sgt.opendata.arcgis.com/pages/conditions-generales-dutilisation

_API faite a but éducative (dans le cadre de l'interopérabilité avec le langage python)_

_je ne suis pas responsable de ce que vous en faite_
