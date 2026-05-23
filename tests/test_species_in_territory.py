"""Phase 2c.2 — species_in_territory."""

from build_territory_species_index import (
    Occurrence,
    Territory,
    species_in_territory,
)


BC_BOX = Territory(
    slug="bc-box", name="BC Box", description="u",
    geometry={
        "type": "Polygon",
        "coordinates": [[
            [-124, 49], [-122, 49], [-122, 50], [-124, 50], [-124, 49],
        ]],
    },
    color="#000",
)


def _occ(species, lat, lon, uncert=15.0):
    return Occurrence(
        species=species, lat=lat, lon=lon, year=2026,
        event_date=None, basis_of_record="HUMAN_OBSERVATION",
        coord_uncertainty_m=uncert, dataset_name=None,
    )


def test_empty_input():
    assert species_in_territory(BC_BOX, []) == []


def test_no_matches():
    occs = [_occ("Zostera marina", 20.0, -100.0)]
    assert species_in_territory(BC_BOX, occs) == []


def test_dedup_and_sort():
    occs = [
        _occ("Pseudotsuga menziesii",   49.3, -123.1),  # in
        _occ("Arctostaphylos uva-ursi", 49.4, -123.0),  # in
        _occ("Pseudotsuga menziesii",   49.5, -122.9),  # in, duplicate species
        _occ("Zostera marina",          20.0, -100.0),  # out
    ]
    assert species_in_territory(BC_BOX, occs) == [
        "Arctostaphylos uva-ursi",
        "Pseudotsuga menziesii",
    ]


def test_uncertainty_filter_drops_sloppy_inside_points():
    occs = [
        _occ("Pseudotsuga menziesii",   49.3, -123.1, uncert=50_000.0),  # in, but sloppy
        _occ("Arctostaphylos uva-ursi", 49.4, -123.0, uncert=None),      # in, unknown
    ]
    assert species_in_territory(BC_BOX, occs) == ["Arctostaphylos uva-ursi"]
