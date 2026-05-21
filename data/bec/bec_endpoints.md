# BEC Map — Service Endpoints

## WMS (Web Map Service) — for map tile overlays
```
https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY/ows?service=WMS&request=GetCapabilities
```
Use this to render BEC zones as a visual layer on Leaflet/MapLibre maps without downloading shapefiles.

## WFS (Web Feature Service) — for data queries
```
https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=pub:WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY&outputFormat=application/json
```
Returns GeoJSON with full polygon geometry + attributes. 15,666 polygons total.

### Key attributes
| Field | Example | Description |
|-------|---------|-------------|
| ZONE | CWH | Zone code |
| ZONE_NAME | Coastal Western Hemlock | Zone full name |
| SUBZONE | ds | Subzone code |
| SUBZONE_NAME | Dry Submaritime | Subzone full name |
| VARIANT | 1 | Variant number (nullable) |
| VARIANT_NAME | Central variant | Variant name (nullable) |
| PHASE | a | Phase code (nullable) |
| MAP_LABEL | CWHds1 | Combined label |
| BGC_LABEL | CWH ds 1 | Spaced label |
| NATURAL_DISTURBANCE | NDT2 | Natural disturbance type code |

### CRS
Default CRS is EPSG:3005 (BC Albers). For web maps, request in EPSG:4326:
```
&srsName=EPSG:4326
```

### Pagination
Use `count` and `startIndex` parameters for pagination. Max features: 15,666.

## ArcGIS REST Service
```
https://delivery.maps.gov.bc.ca/arcgis/rest/services/mpcm/bcgwpub/MapServer/38
```

## Data Summary
- **Version:** 12 (September 2, 2021)
- **Total polygons:** 15,666
- **Unique BEC units:** 213
- **Top-level zones:** 16
- **Licence:** Open Government Licence - British Columbia

## 16 BEC Zones
| Code | Name | Subzone/Variants |
|------|------|-----------------|
| BAFA | Boreal Altai Fescue Alpine | 2 |
| BG | Bunchgrass | 5 |
| BWBS | Boreal White and Black Spruce | 7 |
| CDF | Coastal Douglas-fir | 1 |
| CMA | Coastal Mountain-heather Alpine | 3 |
| CWH | Coastal Western Hemlock | 19 |
| ESSF | Engelmann Spruce – Subalpine Fir | 70 |
| ICH | Interior Cedar – Hemlock | 30 |
| IDF | Interior Douglas-fir | 21 |
| IMA | Interior Mountain-heather Alpine | 2 |
| MH | Mountain Hemlock | 8 |
| MS | Montane Spruce | 13 |
| PP | Ponderosa Pine | 2 |
| SBPS | Sub-Boreal Pine – Spruce | 4 |
| SBS | Sub-Boreal Spruce | 20 |
| SWB | Spruce – Willow – Birch | 6 |
