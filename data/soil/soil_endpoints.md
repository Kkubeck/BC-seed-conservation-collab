# BC Soil Survey — Service Endpoints

## Primary Interface: SIFT (Soil Information Finder Tool)
- **Interactive map:** https://governmentofbc.maps.arcgis.com/apps/MapSeries/index.html?appid=cc25e43525c5471ca7b13d639bbcd7aa
- **Info page:** https://www2.gov.bc.ca/gov/content/environment/air-land-water/land/soil/soil-information-finder

## Data Catalogue
- **Soil Mapping Data Packages:** https://catalogue.data.gov.bc.ca/dataset/soil-mapping-data-packages
- **Soil Survey Spatial View:** https://catalogue.data.gov.bc.ca/dataset/soil-survey-spatial-view

## BC Geographic Warehouse
The soil survey polygons are accessible through the BC Geographic Warehouse custom download:
https://catalogue.data.gov.bc.ca/dataset/soil-survey-spatial-view

## Notes
- Soil data is NOT available as a standard WFS layer on openmaps.gov.bc.ca
- It's served through ArcGIS services via SIFT
- Coverage is NOT province-wide — detailed surveys (1:20K) in agricultural south, coarse mapping (1:250K) elsewhere
- Northern/remote areas may have minimal or no soil survey data
- The Soil Map geodatabase contains 'best available' data with overlapping data removed
- Soil attributes link to soil name and layer files for detailed properties
- Licence: Open Government Licence - British Columbia
- For map overlay: use WMS tile layer from the SIFT ArcGIS service, or download geodatabase
