from .utils.objects import GeoObject, GeoClass

import requests, json

__title__ = 'GeoNC'
__author__ = 'ThePhoenix78'
__license__ = 'MIT'
__copyright__ = 'Copyright 2024-2026 ThePhoenix78'
__url__ = 'https://github.com/ThePhoenix78/GeoNC'
__newest__ = __version__ = '2.0.0'


try:
    with requests.get("https://pypi.python.org/pypi/GeoNC/json") as response:
        __newest__ = json.loads(response.text)["info"]["version"]
except Exception:
    pass

finally:
    del json, requests

if __version__ < __newest__:
    print(f"New version of {__title__} available: {__newest__} (Using {__version__})")
else:
    print(f"version : {__version__}")