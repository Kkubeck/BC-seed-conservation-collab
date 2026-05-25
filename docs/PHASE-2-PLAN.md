# Phase 2 — Prototype "The Map"

Locked plan for the interactive territory → species map. Follows the HtDP
**Analysis Program Recipe** (see `knowledge/design-style-ethic/STYLE.md`):
Phase 1 plans the work, Phase 2 builds it.

Stack choice: extend the existing Quarto site with a Leaflet/OJS map page.
All persistent outputs are GeoJSON + JSON lookup tables — portable to any
future React/MapLibre/Mapbox stack without re-derivation.

---

## Phase 1 — Plan

### 1a. Information available in source files

| Source | Path | Shape | Notes |
|---|---|---|---|
| First Nations territories | `data/territories/bc-territories.geojson` | GeoJSON FeatureCollection, 139 features. Per-feature: `properties.Name`, `Slug`, `ID`, `color`, `description`; `geometry` is `Polygon` or `MultiPolygon` (lon/lat). | Pulled 2026-05-22 via NLD API, filtered to BC bbox. Borders contested by design. |
| BC-native species master list | `data/bc_native_vascan_master.csv` | 2,519 rows; columns: `id, scientificName, family, genus, specificEpithet, infraspecificEpithet, taxonRank, scientificNameAuthorship` | The canonical species universe. |
| GBIF occurrences (sample) | `data/gbif/gbif_sample_occurrences.csv` | 6,000 rows; columns: `species, decimalLatitude, decimalLongitude, year, basisOfRecord, coordinateUncertaintyInMeters, datasetName` | Sample only. Full BC pull is 1.9M occurrences; defer for MVP. |
| Authored species profiles | `species/*.qmd` | 9 files. Filename stem = profile slug (e.g. `arctostaphylos-uva-ursi.qmd`). | These are the only species we currently deep-link to. |
| Propagation protocols | `data/protocols/` | Scoping notes only — `INTEGRATION-NOTES.md`, `SOURCES.md`. No structured records yet. | Out of scope for Phase 2 (Phase 3 work). |

**Not used in Phase 2 MVP, but architecturally accounted for:**
- Indigenous / local names. See [`LOCAL-NAMES-PRINCIPLES.md`](LOCAL-NAMES-PRINCIPLES.md) — `LocalName` and `NameRelationship` are designed as peer data types to `Species`, not fields on it. No local-name data is loaded in Phase 2; the principles doc records the contract that future ingestion must satisfy.

**Not used in Phase 2 MVP** (deferred to a later iteration of the same map page):
- `data/bec/` — BEC zone polygons (toggle stub only)
- `data/soil/` — soil layer (toggle stub only)
- `data/roads/` — roads layer (toggle stub only)

### 1b. Desired output (one sentence)

> An interactive Quarto map page where a user clicks a Nation's territory polygon and sees: the Nation's name, the count and list of BC-native species recorded inside that polygon (from GBIF), and direct links to any authored species profile pages — gated by a sovereignty config that controls per-Nation visibility.

### 1c. Expected output sketch

```
┌─────────────────────────────────────────────────────────────┐
│ [BC map, territory polygons coloured by Nation]              │
│                                                              │
│   user clicks "S'ólh Téméxw (Stó:lō)" polygon                │
│                                                              │
│   Popup ─────────────────────────────────────────┐           │
│   │ S'ólh Téméxw (Stó:lō)                         │           │
│   │ 1,243 BC-native species recorded (GBIF sample)│           │
│   │                                                │           │
│   │ Profiles available (3):                        │           │
│   │  • Arctostaphylos uva-ursi  →                  │           │
│   │  • Symphoricarpos albus     →                  │           │
│   │  • Juniperus scopulorum     →                  │           │
│   │  [show full species list (1,240 more)]         │           │
│   └────────────────────────────────────────────────┘           │
│                                                              │
│  Layer toggles: [✓] Territories  [ ] BEC  [ ] Soil  [ ] Roads│
└─────────────────────────────────────────────────────────────┘
```

For a Nation whose sovereignty config is `nation-only`, the popup shows only
the Nation name and a contact note — no species derivation, no counts.

---

## Phase 2 — Build (to design next, after 1a–1c are locked)

### 2a. Data definitions

To be written in `scripts/build_territory_species_index.py` per HtDP recipe.
Planned types:

1. `Territory` — compound: `(id, slug, name, geometry, color)`
2. `Occurrence` — compound: `(species, lat, lon, year, basis_of_record, coord_uncertainty_m, dataset_name)`
3. `Species` — compound: `(scientific_name, vascan_id, has_profile: bool, profile_slug: Optional[str])`
4. `Visibility` — enumeration: `{"public", "nation-only", "redacted", "delete-on-request"}`. `redacted` and `delete-on-request` have identical effect at build time (slug omitted from output); the distinct label preserves an audit trail when a Nation specifically asked for removal.
5. `TerritorySpeciesIndex` — compound: `{territory_id: {species_count, species_with_profiles, all_species}}`

Each definition will include: type, interpretation comment, ≥1 example, template.

### 2b. Read functions (one per input)

- `read_territories(path) -> List[Territory]`
- `read_occurrences(path) -> List[Occurrence]`
- `read_vascan_master(path) -> List[Species]`
- `read_authored_profiles(dir) -> Set[profile_slug]`
- `read_visibility_config(path) -> Dict[territory_slug, Visibility]`

Each with three tiny fixture files (empty / one-row / multi-row with missing values) before any analysis function runs.

### 2c. Analysis functions

- `point_in_territory(occurrence, territory) -> bool`
- `species_in_territory(territory, occurrences) -> List[scientific_name]`
- `build_index(territories, occurrences, species_master, profiles) -> TerritorySpeciesIndex`
- `apply_sovereignty(index, visibility_config) -> PublicTerritorySpeciesIndex`

### 2d. Map page

`map.qmd` consuming three artifacts:

- `data/territories/bc-territories.geojson` (already exists)
- `data/territory_species_index.json` (built by 2c; gitignored as a build artifact)
- `data/territories/visibility.yml` (sovereignty config — empty by default, every territory resolves to `public`)

OJS code block initializes Leaflet, renders the territory layer, attaches
click handlers that look up the territory in the index, and renders the
popup HTML. Layer toggles are wired as no-op stubs for BEC/soil/roads.

### Portability check

Phase 3+ may swap the view layer (e.g., React + MapLibre, native app, etc.).
The derived `data/territory_species_index.json` and `data/territories/visibility.yml` are the
contract — they live independent of Quarto and remain valid inputs to any
future renderer.
