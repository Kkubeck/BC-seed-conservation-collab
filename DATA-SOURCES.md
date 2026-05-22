# Data Sources Reference

All external data sources used in this project, with endpoints, licensing, and status.

---

## 1. Species Catalog — VASCAN (Canadensys)

| | |
|---|---|
| **What** | Authoritative checklist of all Canadian vascular plants with per-province distribution status (native/introduced/ephemeral/etc.) |
| **Provider** | Canadensys / Université de Montréal |
| **URL** | https://data.canadensys.net/ipt/resource?r=vascan |
| **Download** | Darwin Core Archive (ZIP): `https://data.canadensys.net/ipt/archive.do?r=vascan` |
| **Format** | Tab-separated text files (taxon.txt, distribution.txt, vernacularname.txt) |
| **Records** | 33,662 taxa; 30,346 distribution records |
| **BC scope** | 2,519 BC-native vascular plant taxa (filtered from distribution.txt) |
| **Licence** | CC0 1.0 (Public Domain) |
| **Citation** | Brouillet et al. 2010+. VASCAN, the Database of Vascular Plants of Canada. http://data.canadensys.net/vascan |
| **Status** | ✅ Downloaded, filtered, gap analysis complete |
| **Local path** | `data/vascan/` |

---

## 2. Species Distribution — GBIF

| | |
|---|---|
| **What** | Global occurrence records — geolocated observations and specimen records for biodiversity |
| **Provider** | Global Biodiversity Information Facility |
| **URL** | https://www.gbif.org |
| **API** | `https://api.gbif.org/v1/occurrence/search` (no auth for search; bulk downloads require free account) |
| **BC plant records** | ~1,907,393 georeferenced occurrences (Plantae, British Columbia, with coordinates) |
| **Coverage** | ~98% of our 2,519 target taxa have occurrence records |
| **Key sources** | UBC Herbarium, iNaturalist, BC Conservation Data Centre |
| **Licence** | Varies per dataset (CC0, CC-BY, CC-BY-NC); check per-record `license` field |
| **Citation** | GBIF.org. GBIF Occurrence Download. https://doi.org/10.15468/dl.[KEY] |
| **Status** | ✅ Scoped; 6,000-record sample pulled for 20 species. Full download requires free GBIF account registration. |
| **Local path** | `data/gbif/` |
| **TODO** | Register GBIF account for bulk download of all BC native plant occurrences |

---

## 3. Biogeoclimatic Ecosystem Classification (BEC) Zones

| | |
|---|---|
| **What** | Provincial ecological classification — Zone/Subzone/Variant/Phase polygons covering all of BC |
| **Provider** | BC Ministry of Forests / Government of British Columbia |
| **Catalogue** | https://catalogue.data.gov.bc.ca/dataset/bec-map |
| **WFS** | `https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY/ows` |
| **WMS** | Same endpoint, `service=WMS` — for map tile overlay without downloading geometry |
| **ArcGIS** | `https://delivery.maps.gov.bc.ca/arcgis/rest/services/mpcm/bcgwpub/MapServer/38` |
| **Version** | v12 (September 2, 2021) |
| **Records** | 15,666 polygons; 213 unique BEC units; 16 top-level zones |
| **CRS** | EPSG:3005 (BC Albers); request `srsName=EPSG:4326` for web maps |
| **Licence** | Open Government Licence – British Columbia |
| **Status** | ✅ Zone reference table downloaded; WMS/WFS endpoints documented |
| **Local path** | `data/bec/` |

---

## 4. Soil Survey

| | |
|---|---|
| **What** | Soil survey polygons with type, texture, drainage, parent material, and agricultural capability |
| **Provider** | BC Ministry of Environment / Government of British Columbia |
| **SIFT tool** | https://www2.gov.bc.ca/gov/content/environment/air-land-water/land/soil/soil-information-finder |
| **Catalogue** | https://catalogue.data.gov.bc.ca/dataset/soil-survey-spatial-view |
| **Service** | ArcGIS (via SIFT); NOT available as standard WFS on openmaps.gov.bc.ca |
| **Coverage** | ⚠️ NOT province-wide — detailed surveys (1:20K) in agricultural south; coarse mapping (1:250K) or no data in northern/remote areas |
| **Licence** | Open Government Licence – British Columbia |
| **Status** | ✅ Endpoints documented; data accessible via SIFT ArcGIS or BC Geographic Warehouse download |
| **Local path** | `data/soil/` |

---

## 5. Digital Road Atlas (DRA)

| | |
|---|---|
| **What** | Comprehensive road network — urban, rural, and partial resource roads for all of BC |
| **Provider** | GeoBC / Government of British Columbia |
| **Info** | https://www2.gov.bc.ca/gov/content/data/geographic-data-services/topographic-data/roads |
| **WFS** | `https://openmaps.gov.bc.ca/geo/pub/WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP/ows` |
| **WMS** | Same endpoint, `service=WMS` |
| **Records** | ~905,000 road segments |
| **Update** | Monthly |
| **Licence** | Open Government Licence – British Columbia |
| **Status** | ✅ Endpoints documented |
| **Local path** | `data/roads/` |

---

## 6. Forest Tenure Road Sections

| | |
|---|---|
| **What** | Forestry and logging access roads — specifically resource roads under forest tenure |
| **Provider** | BC Ministry of Forests / Government of British Columbia |
| **Catalogue** | https://catalogue.data.gov.bc.ca/dataset/forest-tenure-road-section-lines |
| **WFS** | `https://openmaps.gov.bc.ca/geo/pub/WHSE_FOREST_TENURE.FTEN_ROAD_SECTION_LINES_SVW/ows` |
| **WMS** | Same endpoint, `service=WMS` |
| **Records** | ~283,624 road segments |
| **Coverage** | ⚠️ BC estimates ~150,000 km of resource roads are MISSING from current government data |
| **Licence** | Open Government Licence – British Columbia |
| **Status** | ✅ Endpoints documented |
| **Local path** | `data/roads/` |

---

## 7. First Nations Territories — Native Land Digital

| | |
|---|---|
| **What** | Indigenous territory boundary polygons (approximate, community-contributed) |
| **Provider** | Native Land Digital (native-land.ca) |
| **API docs** | https://api-docs.native-land.ca |
| **API** | `https://native-land.ca/api/index.php?maps=territories&position=LAT,LON` |
| **Auth** | ⚠️ **API key required** (free) — sign up at https://native-land.ca/auth/signup |
| **Alternative** | ArcGIS hosted layer: https://www.arcgis.com/home/item.html?id=41c4b3b2e139439db4ae9e62ca35b2da |
| **Licence** | CC-BY-SA (Creative Commons Attribution-ShareAlike) |
| **Caveats** | Boundaries are NOT legal boundaries. Overlapping territories are common, and many are contested. These borders did not exist cleanly before settler arrival — our bbox filter intentionally includes any territory that grazes BC so we capture the widest set of potential stakeholders. Some Nations may not be represented. Always engage directly with Nations. |
| **Status** | ✅ Pulled 2026-05-22 — 139 territories intersecting BC bbox |
| **Local path** | `data/territories/bc-territories.geojson` (filtered from global FeatureCollection) |
| **Pull command** | `curl -sSL "https://native-land.ca/api/index.php?maps=territories&key=$KEY"` then filter to BC bbox (lat 48.3–60.0, lon -139.06 to -114.04) |
| **API key** | Stored at `~/.openclaw/workspace/state/secrets/native-land-api-key` (not in repo) |

---

## 8. BC Species & Ecosystems Explorer (BCSEE)

| | |
|---|---|
| **What** | Conservation status, range information, and at-risk listings for 24,000+ BC species and ecological communities |
| **Provider** | BC Conservation Data Centre / Government of British Columbia |
| **URL** | https://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/conservation-data-centre/explore-cdc-data/species-and-ecosystems-explorer |
| **Access** | Web search tool with export; no public API |
| **Licence** | Open Government Licence – British Columbia |
| **Status** | 📋 Identified, not yet integrated |
| **Potential use** | Conservation status enrichment for species catalog (Red/Blue listed, COSEWIC, SARA) |

---

## 9. E-Flora BC

| | |
|---|---|
| **What** | Electronic atlas of BC plants — distribution maps, photos, taxonomic descriptions, biogeography |
| **Provider** | UBC Department of Geography |
| **URL** | https://linnet.geog.ubc.ca/biodiversity/eflora/ |
| **Access** | Web atlas with per-species search; links to BC Ministry official species list |
| **Licence** | Academic use; check individual page terms |
| **Status** | 📋 Identified, not yet integrated |
| **Potential use** | Distribution maps, taxonomic verification, species photos |

---

## Future Data Sources (Not Yet Evaluated)

| Source | Potential Use |
|--------|-------------|
| **iNaturalist** (via GBIF) | Community observations, photos, phenology data |
| **BC Climate Data** (ClimateBC) | Climate normals per BEC unit for propagation planning |
| **Canadian Soil Information Service (CANSIS)** | Federal soil survey data complementing provincial SIFT |
| **World Flora Online** | Global taxonomic backbone for name reconciliation |
| **IUCN Red List** | Global conservation assessments |

---

## Licence Summary

| Source | Licence | Attribution Required |
|--------|---------|---------------------|
| VASCAN | CC0 (Public Domain) | Courtesy citation recommended |
| GBIF | Varies per dataset | Yes — per-download DOI |
| BC Gov layers (BEC, Soil, Roads) | OGL-BC | Yes |
| Native Land Digital | CC-BY-SA | Yes — "Native Land Digital (native-land.ca)" |
| BCSEE | OGL-BC | Yes |
| E-Flora BC | Academic | Check per use |

---

## Propagation Protocols

| | |
|---|---|
| **Top pick** | **Native Plant Network Propagation Protocol Database** |
| **Provider** | RNGR (USDA Forest Service / University of Idaho) |
| **URL** | https://npn.rngr.net/npn/propagation/protocol-database |
| **Access** | Search UI only; no verified public API or bulk download |
| **Coverage** | North America; best broad public source for native plant propagation protocols |
| **Protocol depth** | Propagation method, stock type, collection timing, processing, pretreatment, stratification, growing phases, hardening, references |
| **Licence** | Unknown |
| **Status** | ✅ Verified; best first ingestion target |

| | |
|---|---|
| **Top pick** | **Pacific Northwest Plant Propagation Protocols** |
| **Provider** | University of Washington ESRM 412 via RNGR |
| **URL** | https://rngr.net/resources/pacific-northwest-plant-propagation-protocols |
| **Access** | RNGR page links to a Shiny app; no verified API |
| **Coverage** | Pacific Northwest; very BC-relevant |
| **Protocol depth** | Similar to NPN, with strong regional/ecotype context |
| **Licence** | Unknown |
| **Status** | ✅ Verified; best regional supplement |

| | |
|---|---|
| **Top pick** | **BC Tree Seed Centre / SPAR germination guidance** |
| **Provider** | BC Ministry of Forests |
| **URL** | https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed |
| **Access** | Open web pages/tables; no public bulk protocol dataset confirmed |
| **Coverage** | BC forest tree species |
| **Protocol depth** | Soak hours, stratification days, temperatures, test days, germinator regimes, germination capacity, seeds per gram |
| **Licence** | BC government pages; reuse needs licence check per record/page |
| **Status** | ✅ Verified; highest-value BC-specific tree source |

| | |
|---|---|
| **Strong backfill** | **USDA PLANTS + NRCS Plant Guides** |
| **Provider** | USDA NRCS |
| **URL** | https://plants.sc.egov.usda.gov/ |
| **Access** | Plant profiles and guide PDFs; no unified protocol API |
| **Coverage** | US and territories; many western taxa overlap BC flora |
| **Protocol depth** | Often includes sowing depth, stratification, establishment, greenhouse handling, seeds/kg |
| **Licence** | Plant data are free for use; image rights vary |
| **Status** | ✅ Verified; useful secondary source |

| | |
|---|---|
| **Trait reference** | **Kew Seed Information Database (SID)** |
| **Provider** | Royal Botanic Gardens, Kew |
| **URL** | https://data.kew.org/sid/ |
| **Access** | Legacy public site; no verified public API; related MSBP warehouse is partner-restricted |
| **Coverage** | Global seed biology and MSB-linked collections |
| **Protocol depth** | Strong for dormancy, germination, viability, and storage traits; weaker for full nursery protocols |
| **Licence** | Restricted/unclear |
| **Status** | ✅ Verified; good for normalization and gap-filling, not first-pass ingestion |

---

*Last updated: May 21, 2026*
