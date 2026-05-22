# BC Seed Conservation Collab — Project Vision

**Working title:** BC Native Plant Propagation & Land Stewardship Platform
**Started:** May 20, 2026
**Status:** Planning / architecture

---

## Mission

A publicly funded, publicly available propagation knowledge base for every native vascular plant in British Columbia — with a focus on serving BC First Nations by mapping species to their territories and providing germination protocols for plants of ecological and cultural significance.

Feed data to the BC Provincial Seed Bank. But more importantly: build a warehouse of propagation knowledge that belongs to the public, with First Nations data sovereignty built in from day one.

## The Problem

- BC has ~2,000+ native vascular plant species, ~595 at risk (~30%)
- Propagation protocols exist scattered across institutions, notebooks, and individual expertise
- No centralized, public, freely accessible source of "how to grow BC's native plants"
- First Nations communities lack accessible tools to understand what grows on their territory and how to propagate it
- Institutional conservation work is gatekept by career incentives, not shared freely

## Core Audiences

1. **BC First Nations** — territory-specific species maps + propagation guides for cultural and ecological plants
2. **Provincial Seed Bank** — standardized germination data and yield optimization
3. **Restoration practitioners** — reliable, scalable protocols
4. **Students & researchers** — collaborative contribution platform
5. **Other botanical gardens** — inter-garden protocol sharing

## Data Layers

### 1. Species Catalog (the "what exists")
- **Source:** VASCAN (Canadensys) — authoritative checklist, per-province native/introduced status
- **Scope:** All BC-native vascular plants (~2,000+ taxa)
- UBC's 935 IrisBG-flagged native taxa are a subset

### 2. Propagation Protocols (the "how to grow it")
- **Sources:**
  - 9 hand-authored UBC case studies (current)
  - Propagation card reader OCR extractions (in progress — 12,762 cards)
  - Community/student contributions (future)
  - Published literature (future)
- Structured by Baskin & Baskin dormancy classification (ND, PY, PD, MD, MPD)
- Each protocol: dormancy type, treatment, timing, yield data, nursery codes

### 3. Biogeoclimatic Zones (the "what climate/ecology")
- **Source:** BC BEC Map v12 (Open Canada / BC Gov)
- Zone/Subzone/Variant/Phase polygons
- Links species to their ecological envelope

### 4. Soil (the "what ground")
- **Source:** BC Soil Information Finder Tool (SIFT) / Soil Survey Spatial View
- Soil survey polygons with attribute data (type, capability, parent material)

### 5. Species Distribution (the "where it grows")
- **Sources:** GBIF occurrence records, E-Flora BC distribution maps, BCSEE
- Geolocated observation records — the spatial join layer
- This is what connects species to geography

### 6. First Nations Territory Overlay (the "whose land")
- **Source:** Native Land Digital (GeoJSON API, also ArcGIS)
- Territory boundary polygons for all BC First Nations
- Spatial join: territory polygon ∩ species occurrence = "what grows here"

### 7. Access / Road Network (the "how to get there")
- **Sources:**
  - BC Digital Road Atlas (DRA) — all roads, updated monthly
  - Forest Tenure Road Segment Lines — logging/resource roads
- Note: BC estimates ~150,000 km of resource roads missing from current data
- Practical layer for seed collection planning

### 8. Data Sovereignty Controls (the "who decides")
- **FIRST-CLASS ARCHITECTURAL REQUIREMENT — not an afterthought**
- Per-nation control over spatial data visibility within their territory
- Default: GPS coordinates obscured
- Nation chooses precision level: full coords / grid-cell / territory-level / fully hidden
- Cultural significance flag: Nations can suppress even territory-level species association
- Dual-view: researchers see "species X in [Nation] territory" — pin only with permission

## Architecture (TBD)

### Current state
- Quarto website with 9 species profiles, searchable database, student portal
- GitHub Pages deployment

### Likely evolution
- Quarto site becomes documentation/protocol reference layer
- Interactive web application with map interface needed for:
  - Territory-aware species browsing
  - BEC/soil/road layer toggling
  - Sovereignty permission controls per Nation
  - Protocol contribution workflow
- Spatial database backend (PostGIS or similar)
- API for programmatic access

### Technology candidates (to evaluate)
- **Frontend:** Leaflet/MapLibre GL for map rendering
- **Backend:** Python (FastAPI/Flask) or Node
- **Spatial DB:** PostGIS (PostgreSQL + spatial extensions)
- **Data pipeline:** Python (geopandas, GBIF API, VASCAN downloads)
- **Auth:** Per-nation accounts with territory-scoped permissions
- **Hosting:** TBD — needs to be sustainable/low-cost

## Project Phases (draft)

### Phase 1: Foundation Data Assembly
- [ ] Download VASCAN checklist, filter to BC-native vascular plants → master species list
- [ ] Compare master list against UBC's 935 IrisBG taxa — gap analysis
- [ ] Download BEC zone polygons
- [ ] Download soil survey data
- [ ] Pull GBIF occurrence records for BC native plants
- [ ] Download DRA + forest tenure road data
- [ ] Acquire Native Land Digital territory polygons
- [ ] Design data model / schema

### Phase 2: Prototype — "The Map"
- [ ] Spatial database with species occurrences + territory overlay
- [ ] Basic web map: pick a territory → see what grows there
- [ ] BEC/soil/road layer toggles
- [ ] Sovereignty controls architecture (even if only one test Nation)
- [ ] Link to existing Quarto species profiles where available

### Phase 3: Propagation Data Integration
- [ ] Connect card reader OCR pipeline output
- [ ] Template system for structured protocol entry
- [ ] Map protocols to species catalog entries
- [ ] Yield/success data visualization

### Phase 4: Collaboration & Launch
- [ ] Nation-facing portal with sovereignty controls
- [ ] Contribution workflow for protocols
- [ ] Inter-garden data sharing
- [ ] BC Seed Bank integration

## Key Relationships

- **BC First Nations Nursery**: Testing partners and stakeholder
- **UBC Botanical Garden:** Potential information seed source institution but not intended the gatekeeper
- **BC Provincial Seed Bank:** Potential intended data consumer and collaboration partner
- **HTP/Hort students:** Existing contribution model via student portal

## Political Context

- This project is being built independently using entirely public data using a prototype-first approach
- Centering Indigenous data sovereignty from architecture onward is ethically correct (UNDRIP alignment, funding eligibility)

## Connection to Other Projects

- **Propagation Card Reader** (companion repo): Extracting historical protocols from 12,762 scanned cards → feeds Layer 2
- **ben0** (companion repo): IrisBG analytical pipeline, field registry → species metadata enrichment
- **UBC accession data**: 36,984 accessions, 141,422 items → provenance, collection history

---

*"I just want to save the trees."*
