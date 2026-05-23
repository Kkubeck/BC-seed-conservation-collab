import pytest

from conftest import FIXTURES

from build_territory_species_index import read_visibility_config


def test_empty():
    assert read_visibility_config(FIXTURES / "visibility_empty.yml") == {}


def test_some():
    cfg = read_visibility_config(FIXTURES / "visibility_some.yml")
    assert cfg == {
        "second-with-diacritics": "nation-only",
        "third-multi": "redacted",
    }


def test_invalid_value_raises(tmp_path):
    # Loud failure on misconfiguration: silent fallback to "public" would
    # publicly expose a steward who asked for restriction.
    p = tmp_path / "bad.yml"
    p.write_text("some-slug: open-to-all\n")
    with pytest.raises(ValueError, match="invalid visibility"):
        read_visibility_config(str(p))
