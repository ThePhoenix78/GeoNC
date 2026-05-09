# 🌍 GeoNC

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![New Caledonia](https://img.shields.io/badge/New--Caledonia-Geodata-brightgreen)](https://georep.nc/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENCE)
[![Version](https://img.shields.io/badge/Version-2.2+-blue)](https://pypi.org/project/GeoNC/)

**GeoNC** est une bibliothèque Python permettant d'interagir facilement avec les services de données géographiques de la **Nouvelle-Calédonie**. Elle combine les capacités de **GeorepNC** et **ArcgisNC** pour offrir une interface unifiée, disponible en modes **synchrone** et **asynchrone**.

---

## 🚀 Installation

Vous pouvez installer les dépendances nécessaires via `pip` :

```bash
pip install geonc
```

*Note : La bibliothèque dépend de `requests`, `aiohttp`, `urllib3` et `pyproj`.*

---

## 🏗️ Fonctionnement Interne : Les Objets Dynamiques

L'une des forces de GeoNC est l'utilisation de **`GeoClass`**. Tous les résultats retournés par les services sont encapsulés dans cet objet, ce qui permet une manipulation extrêmement fluide des données.

### Pourquoi GeoClass ?
Les services géographiques renvoient souvent des structures JSON complexes et imbriquées. `GeoClass` transforme ces dictionnaires en objets Python dont les clés deviennent des attributs.

```python
resultat = client.get_adresse(nic="1234")

# 1. Accès par attribut (recommandé, avec auto-complétion dans certains IDE)
print(resultat.parcelle.commune)

# 2. Accès par clé (style dictionnaire classique)
print(resultat["parcelle"]["commune"])

# 3. Export en dictionnaire standard
print(resultat.json)
```

> [!TIP]
> Si une valeur est une liste de dictionnaires, GeoNC convertira automatiquement chaque élément en `GeoClass`.

---

## 💡 Utilisation Rapide

### Mode Synchrone
```python
from geonc.sync import GeoNC

client = GeoNC()

# Recherche par adresse
adresse = client.get_adresse(street="Jean Jaurès", number="10")
print(f"Propriétaire : {adresse.parcelle.proprietaire}")

# Recherche par NIC
parcelle = client.get_nic("12345-6789")
```

### Mode Asynchrone
```python
import asyncio
from geonc.asyn import GeoNC

async def main():
    client = GeoNC()
    
    # Recherche de POI (Points d'Intérêt)
    pois = await client.get_pois(street="Jean Jaures")
    for poi in pois:
        print(f"{poi.name} situé à {poi.address}")

asyncio.run(main())
```

---

## 📖 Référence de l'API

### 🛰️ GeorepNC
Services liés au cadastre et aux adresses officielles (DITTT).

- **`get_adresse(number="", street="", nic="")`** : Informations complètes d'une adresse. Retourne un objet `GeoClass`.
- **`get_adresse_list(number="", street="", nic="")`** : Liste d'adresses correspondant à la recherche.
- **`get_nic(nic)`** : Informations sur un Numéro d'Inventaire Cadastral.
- **`get_coords(x=None, y=None, nic=None)`** : Recherche par coordonnées Lambert NC (EPSG:3163) ou par NIC graphique.
- **`get_info(adresse="")`** : Recherche brute "Fuzzy Search" sur le service parcellaire.
- **`tile_connect()`** : Initialise la connexion HTTPS pour la récupération de tuiles.
- **`get_tile(zoom=0, y=0, x=0, out_border=False, check_out_border=True)`** : Récupère une tuile d'imagerie (PNG/JPEG).

### 🗺️ ArcgisNC
Services de localisation évolués et recherche plein texte (DTSI).

- **`get_localisation(number="", street="", limit=6)`** : Géocodage d'adresses via ArcGIS.
- **`get_cadastre(number="", street="", limit=6)`** : Recherche cadastrale.
- **`get_pois(number="", street="", limit=6)`** : Points d'intérêt (commerces, services, etc.).
- **`get_all(number="", street="")`** : Combine localisation, cadastre et POIs.
- **`search(address, index=None, limit=None, lat=None, lon=None, returntruegeometry=None, postcode=None, citycode=None, address_type=None, city=None, category=None)`** : Recherche universelle puissante.
- **`search_csv(filename, index=None, lat=None, lon=None, postcode=None, citycode=None, category=None, address_type=None, result_columns=None)`** : Recherche par lot via un fichier CSV.
- **`reverse(searchgeom, indexes=None, limit=None, lat=None, lon=None, returntruegeometry=None, postcode=None, citycode=None, address_type=None, city=None, category=None)`** : Geocoding inverse (coordonnées ➡️ adresse).
- **`reverse_csv(filename, indexes=None, lat=None, lon=None, postcode=None, citycode=None, category=None, address_type=None, result_columns=None)`** : Geocoding inverse par lot via un fichier CSV.
- **`get_capabilities()`** : Liste les capacités et services disponibles sur les serveurs ArcGIS NC.

### 🔄 Outils et Utilitaires
GeoNC inclut également des outils pour la gestion de session et les conversions.

- **`to_lambert(x, y)`** : WGS84 (Lat/Lon) ➡️ Lambert NC (EPSG:3163).
- **`to_epsg(x, y)`** : Lambert NC (EPSG:3163) ➡️ WGS84 (Lat/Lon).

---

## ⚖️ Mentions Légales

Cette bibliothèque est un outil indépendant facilitant l'accès aux données publiques. Veuillez respecter les conditions d'utilisation des producteurs de données :
- **Georep** : [cadastre.gouv.nc/a-propos](https://cadastre.gouv.nc/a-propos)
- **ArcGIS NC** : [Conditions Open Data](https://georep-dtsi-sgt.opendata.arcgis.com/)
- **DITTT** : [API Localisation Nouvelle-Calédonie](https://localisation.gouv.nc/api/openapi)

---

_Fait avec ❤️ pour la communauté NC._
