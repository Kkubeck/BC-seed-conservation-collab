from conftest import FIXTURES

from build_territory_species_index import read_authored_profiles


def test_empty_directory():
    assert read_authored_profiles(FIXTURES / "profiles_empty") == set()


def test_some_returns_filename_stems():
    assert read_authored_profiles(FIXTURES / "profiles_some") == {
        "arctostaphylos-uva-ursi",
        "symphoricarpos-albus",
    }
