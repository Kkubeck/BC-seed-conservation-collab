import requests
import json
import pandas as pd

url = "https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY/ows"
params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeName": "pub:WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY",
    "count": "5",
    "outputFormat": "application/json"
}

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
