"""Phase 2c.4 — apply_sovereignty."""

from build_territory_species_index import (
    ProfiledSpecies,
    TerritoryEntry,
    apply_sovereignty,
)


def _entry(name, count):
    return TerritoryEntry(
        visibility="public",
        name=name,
        description_url=f"https://example/{name.lower()}",
        species_count=count,
        occurrence_count=count * 5,
        profiled_species=[
            ProfiledSpecies(
                binomial="Arctostaphylos uva-ursi",
                profile_slug="arctostaphylos-uva-ursi",
                scientific_name_full="Arctostaphylos uva-ursi L.",
                vascan_ids=[4821],
            ),
        ],
        all_species=["Pseudotsuga menziesii"] * count,
        coord_uncertainty_cap_m=10_000,
        built_at="2026-05-22T18:30Z",
    )


IDX = {
    "a": _entry("A", 10),
    "b": _entry("B", 20),
    "c": _entry("C", 30),
    "d": _entry("D", 40),
}


def test_empty_inputs():
    assert apply_sovereignty({}, {}) == {}


def test_default_public_preserved():
    out = apply_sovereignty({"a": IDX["a"]}, {})
    assert out["a"].visibility == "public"
    assert out["a"].species_count == 10
    assert out["a"].name == "A"


def test_full_projection_drops_and_nulls():
    cfg = {
        "b":     "nation-only",
        "c":     "redacted",
        "d":     "delete-on-request",
        "ghost": "nation-only",          # config for slug not in index
    }
    out = apply_sovereignty(IDX, cfg)

    # Public dropped/kept correctly.
    assert set(out.keys()) == {"a", "b"}
    assert "ghost" not in out

    # "a": public, untouched.
    assert out["a"].visibility == "public"
    assert out["a"].species_count == 10
    assert out["a"].all_species is not None
    assert out["a"].profiled_species != []

    # "b": nation-only, counts and lists nulled, metadata preserved.
    b = out["b"]
    assert b.visibility == "nation-only"
    assert b.species_count is None
    assert b.occurrence_count is None
    assert b.all_species is None
    assert b.profiled_species == []
    assert b.name == "B"
    assert b.description_url == "https://example/b"
    assert b.coord_uncertainty_cap_m == 10_000
    assert b.built_at == "2026-05-22T18:30Z"


def test_input_not_mutated():
    cfg = {"a": "nation-only"}
    snapshot_a = IDX["a"]
    out = apply_sovereignty(IDX, cfg)
    # Original index entry must still be public with its original data.
    assert IDX["a"] is snapshot_a
    assert IDX["a"].visibility == "public"
    assert IDX["a"].species_count == 10
    assert out["a"].visibility == "nation-only"
    assert out["a"].species_count is None
