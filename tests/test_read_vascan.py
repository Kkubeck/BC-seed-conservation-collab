from conftest import FIXTURES

from build_territory_species_index import read_vascan_master, Species


def test_empty():
    assert read_vascan_master(FIXTURES / "vascan_empty.csv") == []


def test_one_handles_missing_optionals():
    ss = read_vascan_master(FIXTURES / "vascan_one.csv")
    assert len(ss) == 1
    s = ss[0]
    assert isinstance(s, Species)
    assert s.vascan_id == 9999
    assert s.binomial == "Genus species"
    assert s.infraspecific_epithet is None
    assert s.authorship is None
    # Read function never annotates profile info; that's Phase 2c.
    assert s.has_profile is False
    assert s.profile_slug is None


def test_many_covers_all_three_ranks():
    ss = read_vascan_master(FIXTURES / "vascan_many.csv")
    assert len(ss) == 3
    ranks = [s.taxon_rank for s in ss]
    assert ranks == ["species", "variety", "subspecies"]
    # All three share the same derived binomial.
    assert {s.binomial for s in ss} == {"Arctostaphylos uva-ursi"}
    # The subspecies row has empty authorship -> None.
    assert ss[2].authorship is None
