# BC Road Network — Service Endpoints

## 1. Digital Road Atlas (DRA)
**Total features:** 1933292

### WFS
```
https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP/ows
?service=WFS&version=2.0.0&request=GetFeature
&typeName=pub:WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP
&outputFormat=application/json
```

### WMS
```
https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP/ows
?service=WMS&request=GetCapabilities
```

### Attributes (19 fields)
- `DIGITAL_ROAD_ATLAS_LINE_ID`
- `FEATURE_TYPE`
- `HIGHWAY_EXIT_NUMBER`
- `HIGHWAY_ROUTE_NUMBER`
- `SEGMENT_LENGTH_2D`
- `SEGMENT_LENGTH_3D`
- `ROAD_NAME_ALIAS1`
- `ROAD_NAME_ALIAS2`
- `ROAD_NAME_ALIAS3`
- `ROAD_NAME_ALIAS4`
- `ROAD_NAME_FULL`
- `ROAD_SURFACE`
- `ROAD_CLASS`
- `NUMBER_OF_LANES`
- `DATA_CAPTURE_DATE`
- `FEATURE_CODE`
- `OBJECTID`
- `SE_ANNO_CAD_DATA`
- `FEATURE_LENGTH_M`

---

## 2. Forest Tenure Road Sections
**Total features:** 283624

### WFS
```
https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_TENURE.FTEN_ROAD_SECTION_LINES_SVW/ows
?service=WFS&version=2.0.0&request=GetFeature
&typeName=pub:WHSE_FOREST_TENURE.FTEN_ROAD_SECTION_LINES_SVW
&outputFormat=application/json
```

### WMS
```
https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_TENURE.FTEN_ROAD_SECTION_LINES_SVW/ows
?service=WMS&request=GetCapabilities
```

### Attributes (25 fields)
- `FOREST_FILE_ID`
- `ROAD_SECTION_ID`
- `FEATURE_CLASS_SKEY`
- `ROAD_SECTION_NAME`
- `ROAD_SECTION_LENGTH`
- `RETIREMENT_DATE`
- `SECTION_WIDTH`
- `FEATURE_LENGTH`
- `AMENDMENT_ID`
- `FILE_STATUS_CODE`
- `FILE_TYPE_CODE`
- `FILE_TYPE_DESCRIPTION`
- `GEOGRAPHIC_DISTRICT_CODE`
- `GEOGRAPHIC_DISTRICT_NAME`
- `AWARD_DATE`
- `EXPIRY_DATE`
- `CLIENT_NUMBER`
- `CLIENT_LOCATION_CODE`
- `CLIENT_NAME`
- `LOCATION`
- `LIFE_CYCLE_STATUS_CODE`
- `MAP_LABEL`
- `FEATURE_LENGTH_M`
- `OBJECTID`
- `SE_ANNO_CAD_DATA`

## Notes
- DRA: comprehensive urban + rural + partial resource roads, updated monthly
- Forest Tenure: specifically forestry/logging access roads
- BC estimates ~150,000 km of resource roads MISSING from current data
- Key fields for access planning: road surface type, road class, road status
- Licence: Open Government Licence - British Columbia
