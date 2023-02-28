# GeoNC

Mention légales georep : https://cadastre.gouv.nc/a-propos
Mention légales arcgis : https://georep-dtsi-sgt.opendata.arcgis.com/pages/conditions-generales-dutilisation

### utilisation de l'API

* ##### GeorepNC

* ##### ArcgisNC

* ##### GeoNC


## GeorepNC

### Arguments

* __connect__ : bool = True

### Paramètres

* __geo_conn__ : la connection avec le serveur
* __payload__ : infos pour les requetes (ne pas toucher)
* __request_header__ : header des requetes liées aux demandes vers le serveur
* __coord_headers__ : header des requetes liées aux coordonées
* __nic_header__ : header des requetes liées au NIC


### Méthodes
* __geo_connect__ : permet de lier le client au serveur (automatique)

* __get_info__ _(adresse : str)_ : permet de retourner des infos liées a l'adresse

* __get_adresse_list__ _(numero: str="", street: str="", nic: str="")_ : permet de retourner une liste d'adresse correspondant a la requete

* __get_from_adresse__ _(numero: str="", street: str="", nic="")_ : retourne les informations complètes liées a l'adresse / nic

* __get_from_nic__ _(nic: str)_ : retourne les informations relative au nic

* __get_from_coord__ _(x, y)_ : retourne les informations correspondant aux coordonnées


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

* __get_batiment__ _(numero: str="", street: str="")_ : permet de retourner une liste de batiments correspondant a la requete

* __get_lieu_dit__ _(numero: str="", street: str="")_ : permet de retourner une liste de lieux dit correspondant a la requete

* __get_adresse__ _(numero: str="", street: str="")_ : permet de retourner une liste d'adresses correspondant a la requete

* __get_maritime__ _(numero: str="", street: str="")_ : permet de retourner une liste d'espaces maritime correspondant a la requete

* __get_poi__ _(numero: str="", street: str="")_ : permet de retourner une liste de POI correspondant a la requete

* __get_all__ _(numero: str = "", street: str = "")_ : retourne le résultat (si il existe) de toute les requetes au dessus

## GeoNC

### Une combinaison de GeorepNC et ArcgisNC

### Arguments

* __max__ : int = 6 , le nombre maximum d'éléments dans la réponse
* __connect__ : bool = True

### Paramètres

* __\_to_lambert__ : classe pour transformer du espg (nc) en lambert (universel) (ne pas toucher)
* __\_to_epsg__ : classe pour transformer du lambert (universel) en espg (nc) (ne pas toucher)

### Méthodes
* __to_lambert__ _(x: int, y: int)_ : transforme des coords de espg en lambert, retourne un x y

* __to_epsg__ _(x: int, y: int)_ : transforme des coords de lambert en epsg, retourne un x y

* __get_coords_from_adresse__ _(numero: str="", street: str="")_ : permet de retourner une liste de coordonnées correspondant a l'adresse

* __get_coords_from_batiment__ _(numero: str="", street: str="")_ : permet de retourner une liste de coordonnées correspondant au batiment

* __get_coords_from_lieu_dit__ _(numero: str="", street: str="")_ : permet de retourner une liste de coordonnées correspondant au lieux dit

* __get_coords_from_maritime__ _(numero: str="", street: str="")_ : permet de retourner une liste de coordonnées correspondant a l'espace maritime

* __get_coords_from_poi__ _(numero: str="", street: str="")_ : permet de retourner une liste de coordonnées correspondant au poi

* __get_coords_from_nic__ _(nic: str)_ : permet de retourner une liste de coordonnées correspondant au nic

* __get_coords_from_coords__ _(x, y)_ : permet de retourner une liste de coordonnées correspondant au coordonées entrées


### Exemple de code
```py
from geonc import GeoNC

client = GeoNC()

val1 = client.get_maritime(street="Nouméa")
val2 = client.get_from_nic("xxxxx-xxxx")
val3 = client.get_from_coord(10, 20)

```

_API faite a but éducative, je ne suis pas responsable de ce que vous en faite_
