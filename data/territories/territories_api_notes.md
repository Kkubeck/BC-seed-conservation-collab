# Native Land Digital — API Notes

## API Endpoint
```
GET https://native-land.ca/api/index.php?maps=territories&position=LAT,LON
```
Returns GeoJSON features for territories containing the given point.

## Authentication (REQUIRED as of 2026)
- **API key required** — sign up free at https://native-land.ca/auth/signup
- Include key in requests per: https://api-docs.native-land.ca/get-and-use-your-api-key.md
- No cost — just accountability for who's using the data

## Status
- API key not yet obtained — **TODO: Kevin to sign up and get key**
- Once we have a key, we can pull BC territory polygons
- Territory reference CSV is empty pending API access

## Alternative: ArcGIS Hosted Layer
- BC-specific territories available on ArcGIS: https://www.arcgis.com/home/item.html?id=41c4b3b2e139439db4ae9e62ca35b2da
- May not require API key for read access

## Licence
- Data is CC-BY-SA (Creative Commons Attribution-ShareAlike)
- Attribution required: Native Land Digital (native-land.ca)

## Important Caveats
- Territory boundaries are NOT legal boundaries — they are culturally/historically informed approximations
- Overlapping territories are common and expected
- Some Nations may not be represented or may contest boundaries
- Always engage directly with Nations for land-specific decisions

## Data Sovereignty Note
This data is used as a STARTING POINT for the territory overlay.
In the production platform, each Nation controls their own territory definition
and data visibility within it. Native Land Digital boundaries are defaults
that Nations can override, refine, or reject.
