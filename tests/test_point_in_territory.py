"""Phase 2c.1 — point_in_territory.

Polygon used across tests is a 2x1 degree box covering southwestern BC:
    lon in [-124, -122], lat in [49, 50]
which is the same shape used by territories_one.geojson.
"""

from dataclasses import replace

from build_territory_species_index import (
    DEFAULT_COORD_UNCERTAINTY_CAP_M,
    Occurrence,
    Territory,
    point_in_territory,
)


BC_BOX = Territory(
    slug="bc-box",
    name="BC Box",
    description="https://example/bc-box",
    geometry={
        "type": "Polygon",
        "coordinates": [[
            [-124, 49], [-122, 49], [-122, 50], [-124, 50], [-124, 49],
        ]],
    },
    color="#000000",
)

BASE = Occurrence(
    species="Pseudotsuga menziesii",
    lat=49.3, lon=-123.1, year=2026,
    event_date=None,
    basis_of_record="HUMAN_OBSERVATION",
    coord_uncertainty_m=15.0,
    dataset_name="iNat",
)


def test_inside():
    assert point_in_territory(BASE, BC_BOX) is True


def test_outside():
    assert point_in_territory(replace(BASE, lon=-100.0), BC_BOX) is False


def test_uncertainty_above_cap_excluded():
    sloppy = replace(BASE, coord_uncertainty_m=50_000.0)  # 50 km
    assert point_in_territory(sloppy, BC_BOX) is False


def test_uncertainty_none_is_permissive():
    unknown = replace(BASE, coord_uncertainty_m=None)
    assert point_in_territory(unknown, BC_BOX) is True


def test_uncertainty_at_cap_passes():
    edge = replace(BASE, coord_uncertainty_m=float(DEFAULT_COORD_UNCERTAINTY_CAP_M))
    assert point_in_territory(edge, BC_BOX) is True


def test_custom_cap_lets_sloppy_through():
    sloppy = replace(BASE, coord_uncertainty_m=50_000.0)
    assert point_in_territory(sloppy, BC_BOX, coord_uncertainty_cap_m=100_000) is True


def test_multipolygon_first_lobe():
    multi = Territory(
        slug="multi", name="Multi", description="u",
        geometry={
            "type": "MultiPolygon",
            "coordinates": [
                [[[-125, 50], [-124, 50], [-124, 51], [-125, 51], [-125, 50]]],
                [[[-126, 52], [-125, 52], [-125, 53], [-126, 53], [-126, 52]]],
            ],
        },
        color="#000",
    )
    in_first  = replace(BASE, lon=-124.5, lat=50.5)
    in_second = replace(BASE, lon=-125.5, lat=52.5)
    between   = replace(BASE, lon=-124.5, lat=51.5)  # gap between lobes
    assert point_in_territory(in_first,  multi) is True
    assert point_in_territory(in_second, multi) is True
    assert point_in_territory(between,   multi) is False
