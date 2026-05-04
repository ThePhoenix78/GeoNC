# 🌍 GeoNC

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![New Caledonia](https://img.shields.io/badge/New--Caledonia-Geodata-brightgreen)](https://georep.nc/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENCE)

**GeoNC** est une bibliothèque Python permettant d'interagir facilement avec les services de données géographiques de la **Nouvelle-Calédonie**. Elle combine les capacités de **GeorepNC** et **ArcgisNC** pour offrir une interface unifiée, disponible en modes **synchrone** et **asynchrone**.

---

## 🚀 Installation

Vous pouvez installer les dépendances nécessaires via `pip` :

```bash
pip install -r requirements.txt
```

*Note : Assurez-vous d'avoir `requests`, `aiohttp` et `pyproj` installés.*

---

## 💡 Utilisation Rapide

GeoNC propose deux interfaces : une pour le code classique (synchrone) et une pour le code moderne (asynchrone).

### Mode Synchrone
```python
from geonc.sync import GeoNC

client = GeoNC()

# Recherche par adresse
adresse = client.get_adresse(street="Jean Jaurès", number="10")
print(adresse.ftsAddressLabel)

# Recherche par NIC (Numéro d'Inventaire Cadastral)
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
        print(poi.address)

asyncio.run(main())
```

---

## 📖 Référence de l'API

La classe principale `GeoNC` hérite des méthodes de `GeorepNC` et `ArcgisNC`.

### 🛰️ GeorepNC
Services liés au cadastre et aux adresses officielles de Nouvelle-Calédonie.

- **`get_adresse(number="", street="", nic="")`** : Retourne les informations complètes d'une adresse ou d'un NIC.
- **`get_adresse_list(number="", street="", nic="")`** : Retourne une liste d'adresses correspondant à la requête.
- **`get_nic(nic)`** : Retourne les informations relatives à un Numéro d'Inventaire Cadastral spécifique.
- **`get_coords(x, y, nic)`** : Retourne les informations correspondant à des coordonnées (EPSG:3163) (coords ou NIC).
- **`get_info(adresse)`** : Recherche brute sur le service parcellaire.

### 🗺️ ArcgisNC
Services de localisation, cadastre et points d'intérêt via les serveurs ArcGIS de la DTSI.

- **`get_localisation(number="", street="")`** : Géocodage d'adresses.
- **`get_cadastre(number="", street="")`** : Recherche dans la base cadastrale ArcGIS.
- **`get_pois(number="", street="")`** : Recherche de Points d'Intérêt (POIs).
- **`get_all(number="", street="")`** : Combine les résultats de localisation, cadastre et POI.

### 🔄 Conversions de Coordonnées
GeoNC inclut des outils pour transformer les coordonnées entre le système local (EPSG:3163 - Lambert NC) et le système universel (WGS84).

- **`to_lambert(x, y)`** : Convertit du format local (EPSG:3163) vers WGS84.
- **`to_epsg(x, y)`** : Convertit de WGS84 vers le format local (EPSG:3163).

---

## 🏗️ Structure des Données

Tous les résultats sont encapsulés dans un objet **`GeoClass`**. Cela permet d'accéder aux données comme à des attributs d'objet ou comme à un dictionnaire.

```python
resultat = client.get_adresse(nic="1234")

# Accès par attribut (recommandé)
print(resultat.parcelle.commune)

# Accès par clé (style dictionnaire)
print(resultat["parcelle"]["commune"])

# Export en JSON
print(resultat.json)
```

---

## ⚖️ Mentions Légales

Cette bibliothèque a été créée à but éducatif pour faciliter l'interopérabilité avec le langage Python. L'auteur n'est pas responsable de l'usage fait de cet outil.

Veuillez consulter les conditions d'utilisation des services originaux :
- **Georep** : [cadastre.gouv.nc/a-propos](https://cadastre.gouv.nc/a-propos)
- **ArcGIS NC** : [Conditions Générales d'Utilisation](https://georep-dtsi-sgt.opendata.arcgis.com/pages/conditions-generales-dutilisation)

---

_Fait avec ❤️ pour la communauté NC._
