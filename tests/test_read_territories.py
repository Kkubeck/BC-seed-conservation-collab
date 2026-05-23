from conftest import FIXTURES

from build_territory_species_index import read_territories, Territory


def test_empty():
    assert read_territories(FIXTURES / "territories_empty.geojson") == []


def test_one():
    ts = read_territories(FIXTURES / "territories_one.geojson")
    assert len(ts) == 1
    t = ts[0]
    assert isinstance(t, Territory)
    assert t.slug == "test-nation"
    assert t.name == "Test Nation"
    assert t.description.startswith("https://native-land.ca/")
    assert t.color == "#aabbcc"
    assert t.geometry["type"] == "Polygon"


def test_many_preserves_diacritics_and_multipolygon():
    ts = read_territories(FIXTURES / "territories_many.geojson")
    assert len(ts) == 3
    slugs = [t.slug for t in ts]
    assert slugs == ["first", "second-with-diacritics", "third-multi"]
    # Diacritics preserved verbatim — no normalisation, no slugification of the name.
    assert ts[1].name == "S'ólh Téméxw"
    # MultiPolygon geometry passes through unchanged.
    assert ts[2].geometry["type"] == "MultiPolygon"
    assert len(ts[2].geometry["coordinates"]) == 2
