# GBIF API Notes

## Endpoints Used

### Occurrence Search (no auth required)
```
GET https://api.gbif.org/v1/occurrence/search
```
- Max 300 results per page (use `offset` for pagination)
- Rate limited but generous for single-threaded use
- Filter by: scientificName, stateProvince, country, hasCoordinate, etc.

### Bulk Download (requires free account)
```
POST https://api.gbif.org/v1/occurrence/download/request
```
- Register at https://www.gbif.org/user/profile
- Can request millions of records as a zip file
- Required for production-scale data pulls
- Supports predicate-based filtering (geometry, taxonKey, etc.)

## Key Observations
- Total BC plant occurrences with coords: 1,907,393
- Estimated coverage of our 2,519 taxa: ~98%
- Major data sources: UBC Herbarium, iNaturalist, BC CDC
- For full pull: register GBIF account, use download API
