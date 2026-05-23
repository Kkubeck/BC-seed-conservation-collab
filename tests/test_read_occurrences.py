from datetime import date

from conftest import FIXTURES

from build_territory_species_index import read_occurrences, Occurrence


def test_empty():
    assert read_occurrences(FIXTURES / "occurrences_empty.csv") == []


def test_one():
    os_ = read_occurrences(FIXTURES / "occurrences_one.csv")
    assert len(os_) == 1
    o = os_[0]
    assert isinstance(o, Occurrence)
    assert o.species == "Pseudotsuga menziesii"
    assert o.lat == 49.301068
    assert o.lon == -123.139775
    assert o.year == 2026
    assert o.event_date == date(2026, 5, 14)
    assert o.basis_of_record == "HUMAN_OBSERVATION"
    assert o.coord_uncertainty_m == 15.0
    assert o.dataset_name == "iNaturalist research-grade observations"


def test_many_handles_missing_values():
    os_ = read_occurrences(FIXTURES / "occurrences_many.csv")
    assert len(os_) == 3
    # Row 2: empty eventDate AND empty coordinateUncertaintyInMeters.
    second = os_[1]
    assert second.species == "Arctostaphylos uva-ursi"
    assert second.event_date is None
    assert second.coord_uncertainty_m is None
    assert second.basis_of_record == "PRESERVED_SPECIMEN"
    assert second.dataset_name == "UBC Herbarium"
    # Row 3: empty datasetName.
    third = os_[2]
    assert third.dataset_name is None
    assert third.coord_uncertainty_m == 200.0
