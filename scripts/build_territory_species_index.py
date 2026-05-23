"""
build_territory_species_index.py
================================

Phase 2a deliverable: HtDP-style data definitions for the territory ->
species index that powers the interactive map page (map.qmd).

This file currently contains data definitions only.  Read functions,
analysis functions, and the main entry point follow in Phase 2b and 2c.

Locked data definitions (see docs/PHASE-2-PLAN.md for the surrounding plan):

  1. Territory
  2. Occurrence
  3. Species
  4. Visibility
  5. TerritorySpeciesIndex  (+ TerritoryEntry, ProfiledSpecies)

Recipe reference: knowledge/design-style-ethic/STYLE.md.

Related contract: docs/LOCAL-NAMES-PRINCIPLES.md.  LocalName and
NameRelationship are deliberately NOT defined here; they are peer types
to Species, not fields on it, and are out of scope for Phase 2.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Literal, Optional, Set

import yaml


# =============================================================================
# 1. Territory
# =============================================================================
# Type:
#   Territory = NamedTuple(
#     slug:        str,                     # NLD URL slug, e.g. "stolo".
#                                           #   Canonical join key.  Unique across
#                                           #   the bulk feed; ASCII; URL-safe.
#     name:        str,                     # Display name, may contain
#                                           #   Indigenous orthography & diacritics.
#     description: str,                     # NLD profile URL kept verbatim,
#                                           #   e.g. "https://native-land.ca/maps/territories/stolo".
#                                           #   Not reconstructed, so it survives
#                                           #   upstream slug-scheme changes.
#     geometry:    Geom,                    # GeoJSON Polygon | MultiPolygon,
#                                           #   coordinates (lon, lat),
#                                           #   WGS84 / EPSG:4326.
#     color:       str,                     # NLD-assigned hex, e.g. "#820893".
#   )
#   Geom = Dict   # raw GeoJSON geometry; passed through to Leaflet unchanged.
#
# Interpretation:
#   One First Nations territory polygon as published by Native Land Digital
#   (native-land.ca).  Boundaries are community-asserted, not legal -- overlap
#   and contestation are normal and expected.  We include any territory whose
#   geometry grazes BC so every potential stakeholder is represented;
#   exclusion is a worse error than over-inclusion here.
#
# Example:
#   Territory(
#     slug="cayuse-umatilla-and-walla-walla",
#     name="Cayuse, Umatilla and Walla Walla",
#     description="https://native-land.ca/maps/territories/cayuse-umatilla-and-walla-walla",
#     geometry={"type": "Polygon", "coordinates": [[[-124.28, 47.16]]]},
#     color="#820893",
#   )
#
# Template:
#   def fn_for_territory(t: Territory):
#       return ...(t.slug, t.name, t.description, t.geometry, t.color)

Geom = dict


@dataclass(frozen=True)
class Territory:
    slug: str
    name: str
    description: str
    geometry: Geom
    color: str


# =============================================================================
# 2. Occurrence
# =============================================================================
# Type:
#   Occurrence = NamedTuple(
#     species:              str,            # GBIF-normalised scientific binomial,
#                                           #   e.g. "Pseudotsuga menziesii".
#                                           #   Join key against Species.binomial.
#                                           #   Non-empty.
#     lat:                  float,          # Decimal latitude, WGS84.
#                                           #   BC pull range roughly [48.3, 60.0].
#     lon:                  float,          # Decimal longitude, WGS84.
#                                           #   BC pull range roughly [-139.06, -114.04].
#     year:                 int,            # Observation year.  Always present in
#                                           #   our pulls.  Range [1500, 2100].
#                                           #   When event_date is also set,
#                                           #   year == event_date.year.
#     event_date:           Optional[date], # Full ISO date when GBIF has it.
#                                           #   None when only year is recorded.
#                                           #   Kept for future phenology work
#                                           #   (flowering windows, seasonal
#                                           #   conspicuousness).
#     basis_of_record:      BasisOfRecord,  # See enumeration below.
#     coord_uncertainty_m:  Optional[float],# Radius around (lat, lon) in metres.
#                                           #   None when GBIF lacks the value
#                                           #   (~15% of sample).  Non-negative;
#                                           #   may reach 4e5 (400 km).  Large
#                                           #   values must NOT be used to assert
#                                           #   territory containment -- that
#                                           #   filter lives in Phase 2c.
#     dataset_name:         Optional[str],  # GBIF dataset provenance string.
#                                           #   Optional defensively: GBIF allows
#                                           #   missing values even though our
#                                           #   current sample has none.
#   )
#
#   BasisOfRecord = Enumeration {
#     "PRESERVED_SPECIMEN", "FOSSIL_SPECIMEN", "LIVING_SPECIMEN",
#     "OBSERVATION", "HUMAN_OBSERVATION", "MACHINE_OBSERVATION",
#     "MATERIAL_SAMPLE", "LITERATURE", "MATERIAL_CITATION", "OCCURRENCE",
#   }
#   # GBIF published vocabulary as of 2026-05.
#
# Interpretation:
#   One species-at-place-at-time record from GBIF.  Each row is *evidence* of
#   the species at that point at that time -- not a continuous range.  Phase 2
#   uses occurrences only to derive "species recorded inside territory X"
#   sets, but the type carries enough resolution (event_date, basis_of_record)
#   to support future phenology and provenance work without re-modelling.
#
# Example:
#   Occurrence(
#     species="Pseudotsuga menziesii",
#     lat=49.301068, lon=-123.139775, year=2026,
#     event_date=date(2026, 5, 14),
#     basis_of_record="HUMAN_OBSERVATION",
#     coord_uncertainty_m=15.0,
#     dataset_name="iNaturalist research-grade observations",
#   )
#
# Template:
#   def fn_for_occurrence(o: Occurrence):
#       return ...(o.species, o.lat, o.lon, o.year,
#                  o.event_date,                  # Optional -> caller decides
#                  fn_for_basis(o.basis_of_record),
#                  o.coord_uncertainty_m,         # Optional -> caller decides
#                  o.dataset_name)                # Optional -> caller decides

BasisOfRecord = Literal[
    "PRESERVED_SPECIMEN", "FOSSIL_SPECIMEN", "LIVING_SPECIMEN",
    "OBSERVATION", "HUMAN_OBSERVATION", "MACHINE_OBSERVATION",
    "MATERIAL_SAMPLE", "LITERATURE", "MATERIAL_CITATION", "OCCURRENCE",
]


@dataclass(frozen=True)
class Occurrence:
    species: str
    lat: float
    lon: float
    year: int
    event_date: Optional[date]
    basis_of_record: BasisOfRecord
    coord_uncertainty_m: Optional[float]
    dataset_name: Optional[str]


# =============================================================================
# 3. Species
# =============================================================================
# Type:
#   Species = NamedTuple(
#     vascan_id:             int,           # VASCAN's stable numeric ID, e.g. 5467.
#                                           #   Unique across all 2,519 BC-native
#                                           #   rows.  Identity key for this row.
#     scientific_name_full:  str,           # Full name with authorship, e.g.
#                                           #   "Equisetum fluviatile Linnaeus".
#                                           #   Display value.  Never empty.
#     family:                str,           # Family, e.g. "Equisetaceae".  Never
#                                           #   empty.  Upward join key for
#                                           #   phylogenetic-neighbour lookups.
#     genus:                 str,           # e.g. "Equisetum".  Never empty.
#                                           #   Closer-range upward join key.
#     specific_epithet:      str,           # e.g. "fluviatile".  Never empty.
#     infraspecific_epithet: Optional[str], # e.g. "uva-ursi".  None for straight
#                                           #   species (1,777 / 2,519);
#                                           #   present for 742 var/subsp rows.
#     taxon_rank:            TaxonRank,     # Enumeration: species|variety|subspecies.
#     authorship:            Optional[str], # e.g. "Linnaeus".  None for 22 rows.
#     binomial:              str,           # Derived: f"{genus} {specific_epithet}".
#                                           #   Held on the record so consumers do
#                                           #   not re-derive.  Multiple rows can
#                                           #   share a binomial.  Join key against
#                                           #   GBIF Occurrence.species and against
#                                           #   profile slugs.
#     has_profile:           bool,          # True iff a species/{profile_slug}.qmd
#                                           #   file exists for this binomial.
#                                           #   Inherited by var/subsp that share
#                                           #   a profiled binomial.
#     profile_slug:          Optional[str], # Kebab-case binomial when has_profile,
#                                           #   else None.
#   )
#
#   TaxonRank = Enumeration {"species", "variety", "subspecies"}
#   # No other ranks are present in our pull.
#
# Interpretation:
#   One row from the BC-native VASCAN master list.  We deliberately model rows
#   (not just unique binomials) so that local ecotypes, varieties, hybrids,
#   and subspecies keep individual identity while remaining traceable to the
#   broader binomial / genus / family.  This lets future protocol-discovery
#   code climb the tree: if no propagation protocol exists for this row, look
#   for one against a sibling sharing the binomial, then the genus, then the
#   family.
#
#   Invariants:
#   - vascan_id is unique; binomial is not.
#   - has_profile is False  =>  profile_slug is None.
#   - has_profile is True   =>  profile_slug is the kebab-case binomial AND a
#                              file species/{profile_slug}.qmd existed at
#                              index build time.
#
# Example (one profiled species and a variety inheriting that profile):
#   Species(
#     vascan_id=4821,
#     scientific_name_full="Arctostaphylos uva-ursi (Linnaeus) Sprengel",
#     family="Ericaceae", genus="Arctostaphylos",
#     specific_epithet="uva-ursi", infraspecific_epithet=None,
#     taxon_rank="species",
#     authorship="(Linnaeus) Sprengel",
#     binomial="Arctostaphylos uva-ursi",
#     has_profile=True,
#     profile_slug="arctostaphylos-uva-ursi",
#   )
#
#   Species(
#     vascan_id=4822,
#     scientific_name_full="Arctostaphylos uva-ursi var. coactilis Fernald & J.F.Macbr.",
#     family="Ericaceae", genus="Arctostaphylos",
#     specific_epithet="uva-ursi", infraspecific_epithet="coactilis",
#     taxon_rank="variety",
#     authorship="Fernald & J.F.Macbr.",
#     binomial="Arctostaphylos uva-ursi",
#     has_profile=True,
#     profile_slug="arctostaphylos-uva-ursi",
#   )
#
# Template:
#   def fn_for_species(s: Species):
#       return ...(s.vascan_id, s.scientific_name_full,
#                  s.family, s.genus, s.specific_epithet,
#                  s.infraspecific_epithet,           # Optional -> caller decides
#                  fn_for_taxon_rank(s.taxon_rank),
#                  s.authorship,                      # Optional -> caller decides
#                  s.binomial, s.has_profile,
#                  s.profile_slug)                    # Optional -> caller decides

TaxonRank = Literal["species", "variety", "subspecies"]


@dataclass(frozen=True)
class Species:
    vascan_id: int
    scientific_name_full: str
    family: str
    genus: str
    specific_epithet: str
    infraspecific_epithet: Optional[str]
    taxon_rank: TaxonRank
    authorship: Optional[str]
    binomial: str
    has_profile: bool
    profile_slug: Optional[str]


# =============================================================================
# 4. Visibility
# =============================================================================
# Type:
#   Visibility = Enumeration {
#     "public",
#     "nation-only",
#     "redacted",
#     "delete-on-request",
#   }
#
# Interpretation:
#   The visibility level set for a polygon on the public map.  Party-agnostic:
#   applies to any steward with standing over a polygon -- initially First
#   Nations territories from NLD; future iterations may include BC parcels,
#   private conservancies, land trusts, etc.  Generic shape supports the
#   "same treatment" principle (raised 2026-05-22).  Authority-to-request and
#   ethical grounds live one layer up (in a future VisibilityRequest record).
#
#   Values:
#     "public"             - Render polygon, name, derived species count,
#                            species list, profile links.  Phase 2 MVP default
#                            for unconfigured polygons, on the reasoning that
#                            (a) no engagement yet, (b) underlying data is
#                            already public, (c) the map functions as outreach
#                            to surface public data affected parties may not
#                            know exists.  Flips to "nation-only" the moment
#                            a steward engages, until they affirm "public".
#                            See "berry-patch-coordinates" note below.
#
#     "nation-only"        - Render polygon and steward name; do NOT render
#                            derived species lists or occurrence counts
#                            publicly.  Name retained even though the type is
#                            generalised; describes rendering behaviour, not
#                            the requester.
#
#     "redacted"           - Do not render the polygon at all.  Polygon data is
#                            retained in our files (no silent mutation of the
#                            upstream dataset); the renderer skips it.
#
#     "delete-on-request"  - Steward has asked for full removal from this
#                            repository.  Pipeline deletes and exclusion-lists
#                            so re-pulls do not silently reintroduce the data.
#
#   "Berry-patch-coordinates" note:
#     Fine-grained occurrence data for wild-food species can expose
#     traditional harvest sites to outsiders.  A future iteration will allow
#     visibility per (polygon, species) so a steward can keep most species
#     public while suppressing the few with harvest-risk concerns.  The
#     polygon-level Visibility here is the first-cut control; species-level
#     masking is a follow-up.
#
#   Authority-to-request:
#     Out of scope for Phase 2.  Captured as a Phase 4 design question: who,
#     on behalf of a Nation or landholding entity, has standing to change
#     Visibility for a given polygon?  The data type does not encode this.
#
# Example:
#   v = "public"
#   v = "nation-only"
#   v = "redacted"
#   v = "delete-on-request"
#
# Template:
#   def fn_for_visibility(v: Visibility):
#       if v == "public":              return ...
#       elif v == "nation-only":       return ...
#       elif v == "redacted":          return ...
#       elif v == "delete-on-request": return ...

Visibility = Literal["public", "nation-only", "redacted", "delete-on-request"]


# =============================================================================
# 5. TerritorySpeciesIndex  (+ TerritoryEntry, ProfiledSpecies)
# =============================================================================
# Type:
#   TerritorySpeciesIndex = Dict[territory_slug: str, TerritoryEntry]
#                           # Keyed by Territory.slug.  Missing keys mean the
#                           # territory was filtered out (redacted /
#                           # delete-on-request) or never built.  Renderers
#                           # must not crash on a polygon whose slug is
#                           # absent -- they fall back to a name-only popup.
#
#   TerritoryEntry = NamedTuple(
#     visibility:              Visibility,        # Drives renderer behaviour.
#     name:                    str,               # Mirrors Territory.name so the
#                                                 #   popup needs no second lookup.
#     description_url:         str,               # Mirrors Territory.description.
#     species_count:           Optional[int],     # Distinct binomials whose GBIF
#                                                 #   occurrences fall inside the
#                                                 #   polygon, after the coord-
#                                                 #   uncertainty filter.  None
#                                                 #   when visibility == "nation-only".
#     occurrence_count:        Optional[int],     # Raw qualifying occurrence count
#                                                 #   (pre-dedup).  None when
#                                                 #   nation-only.
#     profiled_species:        List[ProfiledSpecies],
#                                                 # Subset of all_species with an
#                                                 #   authored species/*.qmd
#                                                 #   profile, link metadata
#                                                 #   pre-resolved for popup
#                                                 #   rendering.  Empty list when
#                                                 #   none qualify OR when nation-only.
#     all_species:             Optional[List[str]],
#                                                 # Every distinct binomial recorded
#                                                 #   in the polygon, alphabetised.
#                                                 #   None when nation-only.
#     coord_uncertainty_cap_m: int,               # Threshold the build used --
#                                                 #   occurrences with
#                                                 #   coord_uncertainty_m greater
#                                                 #   than this were excluded.
#                                                 #   Default 1000 (1 km): keeps
#                                                 #   iNat research-grade points
#                                                 #   and most specimens, excludes
#                                                 #   county-scale records.
#                                                 #   Surfaced on the entry so the
#                                                 #   popup can declare it.
#     built_at:                str,               # ISO-8601 UTC, e.g.
#                                                 #   "2026-05-22T18:30Z".
#                                                 #   Provenance for "last
#                                                 #   updated ..." display.
#   )
#
#   ProfiledSpecies = NamedTuple(
#     binomial:             str,               # e.g. "Arctostaphylos uva-ursi".
#     profile_slug:         str,               # e.g. "arctostaphylos-uva-ursi".
#     scientific_name_full: str,               # Full name w/ authorship for
#                                              #   tooltip/hover display.
#     vascan_ids:           List[int],         # All VASCAN rows sharing this
#                                              #   binomial (species + var + subsp).
#                                              #   Lets the popup say e.g.
#                                              #   "(species + 2 varieties)".
#   )
#
# Interpretation:
#   The pre-computed lookup the map page reads to answer "user clicked
#   territory X -- what should the popup show?"  Built once per data refresh
#   from the inputs in docs/PHASE-2-PLAN.md section 1a, then served as a
#   single static JSON.  Phase 2 ships ONE such index (post-sovereignty,
#   public-safe).  A raw pre-sovereignty version is held build-time only and
#   is never written to the served path -- enforced by build pipeline, not
#   by hope.
#
#   Invariants:
#   - When entry.visibility == "public":
#       species_count, occurrence_count, all_species are populated.
#       profiled_species may be empty but is a list.
#   - When entry.visibility == "nation-only":
#       species_count, occurrence_count, all_species are all None.
#       profiled_species is the empty list.
#       Only polygon, name, and description_url are exposed.
#   - When entry.visibility in {"redacted", "delete-on-request"}:
#       The slug does NOT appear in the index at all.
#   - coord_uncertainty_cap_m and built_at are constant within a single build
#     pass.  They live on the entry only because a flat JSON is simpler than
#     a wrapping object; can be hoisted later if useful.
#
# Example (abbreviated):
#   index = {
#     "stolo": TerritoryEntry(
#       visibility="public",
#       name="S'olh Temexw (Sto:lo)",
#       description_url="https://native-land.ca/maps/territories/stolo",
#       species_count=1243,
#       occurrence_count=8917,
#       profiled_species=[
#         ProfiledSpecies(
#           binomial="Arctostaphylos uva-ursi",
#           profile_slug="arctostaphylos-uva-ursi",
#           scientific_name_full="Arctostaphylos uva-ursi (Linnaeus) Sprengel",
#           vascan_ids=[4821, 4822, 4823],
#         ),
#       ],
#       all_species=["Abies amabilis", "Abies grandis", "Zostera marina"],
#       coord_uncertainty_cap_m=1000,
#       built_at="2026-05-22T18:30Z",
#     ),
#     "some-nation-only-slug": TerritoryEntry(
#       visibility="nation-only",
#       name="(Nation name)",
#       description_url="https://native-land.ca/maps/territories/...",
#       species_count=None, occurrence_count=None,
#       profiled_species=[], all_species=None,
#       coord_uncertainty_cap_m=1000,
#       built_at="2026-05-22T18:30Z",
#     ),
#     # "redacted-slug" intentionally absent.
#   }
#
# Template:
#   def fn_for_index(idx: TerritorySpeciesIndex):
#       acc = ...
#       for slug, entry in idx.items():
#           acc = ...(slug, fn_for_entry(entry), acc)
#       return acc
#
#   def fn_for_entry(e: TerritoryEntry):
#       return ...(fn_for_visibility(e.visibility),
#                  e.name, e.description_url,
#                  e.species_count,                   # Optional
#                  e.occurrence_count,                # Optional
#                  fn_for_profiled_species_list(e.profiled_species),
#                  e.all_species,                     # Optional
#                  e.coord_uncertainty_cap_m, e.built_at)
#
#   def fn_for_profiled_species(p: ProfiledSpecies):
#       return ...(p.binomial, p.profile_slug,
#                  p.scientific_name_full, p.vascan_ids)


@dataclass(frozen=True)
class ProfiledSpecies:
    binomial: str
    profile_slug: str
    scientific_name_full: str
    vascan_ids: List[int]


@dataclass(frozen=True)
class TerritoryEntry:
    visibility: Visibility
    name: str
    description_url: str
    species_count: Optional[int]
    occurrence_count: Optional[int]
    profiled_species: List[ProfiledSpecies]
    all_species: Optional[List[str]]
    coord_uncertainty_cap_m: int
    built_at: str


TerritorySpeciesIndex = Dict[str, TerritoryEntry]


# =============================================================================
# Phase 2b — Read functions
# =============================================================================
# Each read function is pure I/O over one source file.  No joins, no
# enrichment, no annotation -- those live in Phase 2c so reads stay
# trivially testable against fixtures.  HtDP fixtures live in
# tests/fixtures/, three flavours per source (empty / one / many).


def read_territories(path: str) -> List[Territory]:
    # Signature: str -> List[Territory]
    # Purpose:   Load a GeoJSON FeatureCollection from `path` and return one
    #            Territory per feature.  Properties expected:
    #            Slug, Name, description, color.  Geometry is passed through
    #            unchanged as a dict (Leaflet consumes it directly).
    # Examples:  read_territories("tests/fixtures/territories_empty.geojson")
    #              -> []
    #            read_territories("tests/fixtures/territories_one.geojson")
    #              -> [Territory(slug="test-nation", ...)]
    # Template:  arbitrary-sized (loop over features.values, accumulate).
    with open(path) as f:
        doc = json.load(f)
    acc: List[Territory] = []
    for feature in doc.get("features", []):
        props = feature.get("properties", {}) or {}
        acc.append(Territory(
            slug=props["Slug"],
            name=props["Name"],
            description=props.get("description", "") or "",
            geometry=feature.get("geometry", {}) or {},
            color=props.get("color", "") or "",
        ))
    return acc


def read_occurrences(path: str) -> List[Occurrence]:
    # Signature: str -> List[Occurrence]
    # Purpose:   Load a GBIF-style CSV from `path` and return one Occurrence
    #            per row.  Expected columns (extras ignored): species,
    #            decimalLatitude, decimalLongitude, year, eventDate (optional
    #            column; absent in current sample), basisOfRecord,
    #            coordinateUncertaintyInMeters, datasetName.
    #            Empty CSV cells map to None for Optional fields.  Type
    #            coercion is the only logic applied here.
    # Examples:  read_occurrences("tests/fixtures/occurrences_empty.csv")
    #              -> []
    #            read_occurrences(many).len == 3 and second row has
    #              event_date=None, coord_uncertainty_m=None
    # Template:  arbitrary-sized over DictReader rows.
    with open(path) as f:
        rows = list(csv.DictReader(f))
    acc: List[Occurrence] = []
    for row in rows:
        acc.append(Occurrence(
            species=row["species"],
            lat=float(row["decimalLatitude"]),
            lon=float(row["decimalLongitude"]),
            year=int(row["year"]),
            event_date=_parse_iso_date(row.get("eventDate")),
            basis_of_record=row["basisOfRecord"],  # trusted; GBIF vocab
            coord_uncertainty_m=_parse_optional_float(row.get("coordinateUncertaintyInMeters")),
            dataset_name=row.get("datasetName") or None,
        ))
    return acc


def read_vascan_master(path: str) -> List[Species]:
    # Signature: str -> List[Species]
    # Purpose:   Load the BC-native VASCAN master CSV from `path`.  Every row
    #            yields one Species with has_profile=False, profile_slug=None.
    #            Profile annotation is a Phase 2c analysis step, intentionally
    #            kept out of the read function so reads remain pure I/O.
    # Examples:  read_vascan_master("tests/fixtures/vascan_empty.csv") -> []
    #            read_vascan_master(one).len == 1 and that row has
    #              infraspecific_epithet=None, authorship=None, has_profile=False
    # Template:  arbitrary-sized over DictReader rows.
    with open(path) as f:
        rows = list(csv.DictReader(f))
    acc: List[Species] = []
    for row in rows:
        genus = row["genus"]
        epithet = row["specificEpithet"]
        acc.append(Species(
            vascan_id=int(row["id"]),
            scientific_name_full=row["scientificName"],
            family=row["family"],
            genus=genus,
            specific_epithet=epithet,
            infraspecific_epithet=row.get("infraspecificEpithet") or None,
            taxon_rank=row["taxonRank"],            # trusted vs enum
            authorship=row.get("scientificNameAuthorship") or None,
            binomial=f"{genus} {epithet}",
            has_profile=False,
            profile_slug=None,
        ))
    return acc


def read_authored_profiles(species_dir: str) -> Set[str]:
    # Signature: str -> Set[str]
    # Purpose:   Return the set of profile slugs found in `species_dir`, one
    #            per *.qmd file (filename stem).  Used by Phase 2c to
    #            annotate Species rows with has_profile / profile_slug.
    # Examples:  read_authored_profiles("tests/fixtures/profiles_empty") -> set()
    #            read_authored_profiles("tests/fixtures/profiles_some")
    #              -> {"arctostaphylos-uva-ursi", "symphoricarpos-albus"}
    # Template:  arbitrary-sized over Path.glob results.
    return {p.stem for p in Path(species_dir).glob("*.qmd")}


def read_visibility_config(path: str) -> Dict[str, Visibility]:
    # Signature: str -> Dict[territory_slug, Visibility]
    # Purpose:   Load the per-slug visibility overrides from a YAML file.
    #            Missing keys at lookup time mean "use the Phase 2 default"
    #            ("public") -- that resolution happens in 2c, not here.
    #            Validates that every value is a member of the Visibility
    #            enumeration; raises ValueError otherwise (loud failure on
    #            misconfiguration beats silent "public" exposure of a Nation
    #            that asked for restriction).
    # Examples:  read_visibility_config("tests/fixtures/visibility_empty.yml") -> {}
    #            read_visibility_config("tests/fixtures/visibility_some.yml")
    #              -> {"second-with-diacritics": "nation-only",
    #                  "third-multi": "redacted"}
    # Template:  compound (dict) -> validate each pair -> compound.
    with open(path) as f:
        loaded = yaml.safe_load(f)
    if loaded is None:                              # empty file
        return {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path}: expected a YAML mapping at the top level")
    valid = {"public", "nation-only", "redacted", "delete-on-request"}
    out: Dict[str, Visibility] = {}
    for slug, value in loaded.items():
        if value not in valid:
            raise ValueError(
                f"{path}: slug {slug!r} has invalid visibility {value!r}; "
                f"must be one of {sorted(valid)}"
            )
        out[str(slug)] = value
    return out


# ---------------------------------------------------------------------------
# Small helpers — kept private (leading underscore) and minimal.
# These exist only to keep the read functions' bodies linear; they have no
# data definition of their own beyond their docstrings.
# ---------------------------------------------------------------------------

def _parse_optional_float(value: Optional[str]) -> Optional[float]:
    # str|None -> Optional[float].  Empty/None -> None; otherwise float(value).
    if value is None or value == "":
        return None
    return float(value)


def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    # str|None -> Optional[date].  Accepts full ISO date "YYYY-MM-DD".
    # Anything else (year-only, year-month, empty, None) -> None.
    if value is None or value == "":
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


# =============================================================================
# Analysis functions and main(): Phase 2c — next.
# =============================================================================
