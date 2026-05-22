# Integration Notes

## Pull First

1. **Native Plant Network Propagation Protocol Database**
   Best balance of taxonomic breadth and protocol depth for a public-facing restoration knowledge base. It is the most likely source to cover BC native forbs, shrubs, graminoids, and wetland plants that are absent from forestry sources.
2. **Pacific Northwest Plant Propagation Protocols**
   Strong regional fit and likely the fastest way to improve BC relevance. Treat as a companion source to NPN, not a replacement.
3. **BC Tree Seed Centre**
   Pull separately for tree taxa. It gives BC-specific treatment logic and test-condition tables that are more operationally useful than generic literature.

## Second Wave

- **USDA PLANTS + Plant Guides** for overlapping western taxa and missing sowing/establishment details.
- **Kew SID** for dormancy, viability, storage, and seed-trait normalization where full protocols are thin.
- **Semantic Scholar API** for targeted literature searches on uncovered taxa.

## Ingestion Difficulty

| Source | Difficulty | Why |
|---|---|---|
| Native Plant Network | Medium | Searchable public site, but no verified bulk export/API. Likely scraper plus page-level parsing. |
| Pacific Northwest Plant Propagation Protocols | Medium | Shiny app and linked PDFs; likely scrapeable, but identifiers and stable URLs may need curation. |
| BC Tree Seed Centre | Low-medium | Pages are open and tables are structured, but scope is narrow and some values are embedded in prose/PDFs. |
| USDA Plant Guides | Medium-high | Valuable content sits in PDFs with inconsistent formatting. |
| Kew SID | High | Legacy/retired system, unclear bulk access, partial partner-only ecosystem. |
| Semantic Scholar | Medium | API is clean, but extracting protocol facts from papers is the hard part. |

## Normalization Strategy

Build a unified `propagation_protocols` schema around **claims**, not source-specific layouts.

Suggested top-level fields:

| Field | Notes |
|---|---|
| `protocol_id` | Internal stable ID |
| `taxon_name_submitted` | Name as published by source |
| `taxon_name_matched` | Accepted project name after reconciliation |
| `taxon_id` | Project taxon key tied to VASCAN |
| `source_name` | NPN, BC TSC, USDA, etc. |
| `source_url` | Canonical record URL |
| `source_citation` | Plain-text citation |
| `geography_scope` | BC / PNW / North America / global |
| `ecotype_or_provenance` | Source population notes when present |
| `propagation_goal` | plants, plugs, bareroot, seed increase, etc. |
| `propagation_method` | seed / cutting / division / rhizome / other |
| `dormancy_class_raw` | Verbatim source text |
| `dormancy_class_normalized` | Controlled vocabulary mapped to Baskin & Baskin |
| `pretreatments` | Array of treatment steps with type, order, temperature, duration, moisture, chemistry |
| `germination_conditions` | Light, alternating temperature, constant temperature, chamber regime, test duration |
| `sowing` | Depth, substrate, container type, season, spacing |
| `performance` | Germination %, viability %, seeds/kg, seeds/g, storage longevity |
| `nursery_phases` | Establishment, active growth, hardening, outplanting |
| `evidence_level` | operational protocol / literature-derived / student protocol / trait-only |
| `notes` | Free-text caveats |

Recommended controlled vocabularies:

- `propagation_method`: `seed`, `cutting`, `division`, `rhizome`, `bulb/corm`, `transplant`, `unknown`
- `pretreatment.type`: `cold_moist_stratification`, `warm_moist_stratification`, `dry_afterripening`, `scarification_mechanical`, `scarification_chemical`, `leaching`, `soaking`, `smoke`, `heat`, `hormone`, `none`, `other`
- `dormancy_class_normalized`: start with simple buckets aligned to Baskin & Baskin: `ND`, `PY`, `PD`, `MPD`, `MD`, `combinational`, `unknown`

## Name Reconciliation

Use **VASCAN as the canonical taxonomic backbone** for the site.

Matching order:

1. Exact accepted scientific name match to VASCAN BC-native taxa.
2. Source synonym to VASCAN accepted name.
3. Genus-level manual review queue.
4. Exclude cultivars/non-native stock unless explicitly needed.

Keep both submitted and matched names. Do not overwrite source taxonomy.

## Practical Build Sequence

1. Ingest 25-50 pilot taxa from NPN/UW across growth forms: tree, shrub, forb, graminoid, wetland species.
2. Add BC Tree Seed Centre records for all BC-native tree taxa in scope.
3. Design Quarto display around normalized treatment steps plus original-source notes.
4. Only after the schema survives real records, expand with USDA PDFs and literature mining.

## Main Risk

The hard problem is not finding protocol text. It is **normalizing inconsistent prose into comparable treatment steps** without flattening away critical nuance like ecotype, storage age, or whether a treatment is lab-testing versus nursery production. Preserve verbatim source text alongside normalized fields from day one.
