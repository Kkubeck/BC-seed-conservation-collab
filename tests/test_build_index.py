"""Phase 2c.3 — build_index."""

from datetime import datetime, timezone

from build_territory_species_index import (
    Occurrence,
    Species,
    Territory,
    TerritoryEntry,
    build_index,
)


T_BC = Territory(
    slug="bc", name="BC Box", description="https://example/bc",
    geometry={
        "type": "Polygon",
        "coordinates": [[
            [-124, 49], [-122, 49], [-122, 50], [-124, 50], [-124, 49],
        ]],
    },
    color="#111",
)

T_EAST = Territory(
    slug="east", name="East Box", description="https://example/east",
    geometry={
        "type": "Polygon",
        "coordinates": [[
            [-100, 49], [-98, 49], [-98, 50], [-100, 50], [-100, 49],
        ]],
    },
    color="#222",
)


def _occ(species, lat, lon):
    return Occurrence(
        species=species, lat=lat, lon=lon, year=2026,
        event_date=None, basis_of_record="HUMAN_OBSERVATION",
        coord_uncertainty_m=15.0, dataset_name=None,
    )


def _sp(vid, binomial, rank="species", profile_name=None):
    genus, epithet = binomial.split(" ", 1)
    return Species(
        vascan_id=vid,
        scientific_name_full=profile_name or f"{binomial} L.",
        family="Testaceae", genus=genus, specific_epithet=epithet,
        infraspecific_epithet=None, taxon_rank=rank,
        authorship="L.", binomial=binomial,
        has_profile=False, profile_slug=None,
    )


FROZEN = datetime(2026, 5, 22, 18, 30, tzinfo=timezone.utc)


def test_empty_everything():
    assert build_index([], [], [], set(), now=FROZEN) == {}


def test_one_territory_no_occurrences():
    idx = build_index([T_BC], [], [], set(), now=FROZEN)
    e = idx["bc"]
    assert e.visibility == "public"
    assert e.species_count == 0
    assert e.occurrence_count == 0
    assert e.all_species == []
    assert e.profiled_species == []
    assert e.coord_uncertainty_cap_m == 10_000
    assert e.built_at == "2026-05-22T18:30Z"
    assert e.name == "BC Box"
    assert e.description_url == "https://example/bc"


def test_many_with_profile_collapse():
    occs = [
        _occ("Pseudotsuga menziesii",   49.3, -123.1),  # in BC
        _occ("Arctostaphylos uva-ursi", 49.4, -123.0),  # in BC
        _occ("Pseudotsuga menziesii",   49.5, -122.9),  # in BC, dup species
        _occ("Zostera marina",          49.3,  -99.0),  # in East only
    ]
    master = [
        _sp(4821, "Arctostaphylos uva-ursi"),                          # species row
        _sp(4822, "Arctostaphylos uva-ursi", rank="variety"),          # var row
        _sp(5001, "Pseudotsuga menziesii"),                            # not profiled
        _sp(9001, "Zostera marina"),                                   # not profiled
    ]
    profiles = {"arctostaphylos-uva-ursi"}

    idx = build_index([T_BC, T_EAST], occs, master, profiles, now=FROZEN)

    bc = idx["bc"]
    assert bc.occurrence_count == 3
    assert bc.species_count == 2
    assert bc.all_species == [
        "Arctostaphylos uva-ursi",
        "Pseudotsuga menziesii",
    ]
    assert len(bc.profiled_species) == 1
    ps = bc.profiled_species[0]
    assert ps.binomial == "Arctostaphylos uva-ursi"
    assert ps.profile_slug == "arctostaphylos-uva-ursi"
    assert ps.vascan_ids == [4821, 4822]               # species + variety merged
    # scientific_name_full prefers the canonical "species" row.
    assert ps.scientific_name_full == "Arctostaphylos uva-ursi L."

    east = idx["east"]
    assert east.occurrence_count == 1
    assert east.all_species == ["Zostera marina"]
    assert east.profiled_species == []                 # not profiled


def test_built_at_format_uses_utc_when_now_omitted():
    idx = build_index([T_BC], [], [], set())
    # We don't assert exact value, just shape: "YYYY-MM-DDTHH:MMZ".
    s = idx["bc"].built_at
    assert len(s) == 17 and s.endswith("Z") and s[4] == "-" and s[10] == "T"
