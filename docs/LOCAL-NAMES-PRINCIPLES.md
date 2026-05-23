# Local Names — Design Principles

How this project will represent Indigenous, local, and community-held names
for plants. Written **before** any local-name data has been ingested, so the
architecture is shaped by these principles rather than retrofitted to a
quick first implementation.

This document is a contract with future contributors — including Nations who
may bring their own naming data — about what the data structure will and
will not do on their behalf.

---

## The problem we are trying not to cause

The default move in a botanical database is to add an `indigenous_name`
field (or worse, `common_name_indigenous`) onto the species record. That
shape encodes two unstated claims:

1. The Linnaean binomial is the **real** identity of the plant; Indigenous
   names are descriptive labels attached to it.
2. There is a clean **one-to-one** correspondence between an Indigenous name
   and a Linnaean species.

Both claims are false, and the second is often empirically false in ways
that matter. Indigenous plant-naming systems can:

- **Clump** several Linnaean taxa under one name (e.g., a single term that
  covers what botany splits into a species and its variety, or two related
  genera used the same way).
- **Narrow** more finely than Linnaeus — a named ecotype, growth-form, or
  habitat-specific phenotype that VASCAN treats as one species.
- **Overlap partially** with Linnaean groupings without being a subset or
  superset of any one.
- Not refer to a botanical entity at all, but to a use-context, a season,
  or a relational concept that includes the plant.

A `string` field on `Species` cannot represent any of these honestly. It
silently squashes them all into "equivalent translation," which is the same
epistemic move that justifies extracting Indigenous knowledge as if it were
Western data in a different costume.

## What we will do instead

Local names are a **peer data type** to `Species`, not a field on it. The
two relate through an **explicit relationship type** that records the
cardinality and semantic kind of the mapping. The Linnaean binomial keeps
being our indexing key for VASCAN and GBIF — because that is what those
datasets are — but it is no longer the *anchor of meaning*. It is one
projection among others.

In the UI, a territory popup will show local-name records associated with
that Nation alongside (not under) the binomial-keyed species list.

## The data contract (target shape)

These are the types that will be implemented when local-name data is
actually contributed. Each type follows the HtDP recipe (data definition,
interpretation, example, template). Sketch only here — full definitions
will live next to `Species` in `scripts/`.

### `LocalName`
A single name as held by a community, in a language, with provenance and a
visibility level. Fields:

- `nation_slug` — joins to `Territory.slug` so the name is anchored to a
  specific Nation, not abstracted into "Indigenous".
- `language` — ISO 639-3 when available; free-text otherwise. Some Nations
  have multiple dialects or writing systems; recorded here, not coerced.
- `name` — UTF-8 verbatim. **Never slugified, never ASCII-folded, never
  normalised away from the orthography the community supplied.** This
  includes diacritics, syllabics, glottal stops, underdots, lateral
  fricatives, and any other character the source uses.
- `transliteration` — only present if the originating community supplies a
  romanisation. We never invent one.
- `pronunciation_note` — free-text guidance from the source.
- `submitted_by` — who contributed: a person, a Nation office, a published
  source with citation. Provenance is required, not optional.
- `visibility` — see `NationVisibility` (next definition in the data spec).
  Some names are public, some restricted, some sacred and not to be stored
  in this system at all. The default is **restricted** until a Nation
  affirms otherwise.
- `notes` — free text.

### `NameRelationship`
The explicit, typed link between a `LocalName` and zero-or-more VASCAN rows.

- `local_name_id` — foreign key to `LocalName`.
- `vascan_ids` — list of `Species.vascan_id` values. Can be empty (the name
  has no community-attested mapping yet), one (equivalence or narrowing),
  or many (clumping).
- `kind` — one of:
  - `equivalent` — community-attested 1:1 mapping to one Linnaean concept.
  - `clumps` — one LocalName covers several Linnaean taxa.
  - `narrows` — LocalName picks out a finer distinction (ecotype,
    growth-form) than VASCAN expresses.
  - `overlaps` — partial overlap; neither subset.
  - `unknown` — name recorded; mapping not yet attested.
- `notes` — free text, including any ecological / use / relational context
  that the community supplies along with the mapping.

The `kind` field is what carries the structural honesty. Without it the
relationship table would silently collapse into "equivalent" and we would
be back where we started.

## Rules we commit to

1. **No invented mappings.** If a `NameRelationship` is `equivalent` or
   `clumps` or `narrows`, the source must be community-attested. `unknown`
   is the honest default.
2. **No invented orthography.** Names are stored as supplied. No
   silent normalisation, transliteration, or capitalisation changes.
3. **Visibility defaults to restricted.** A `LocalName` record without an
   explicit affirmation that it may be shared publicly is treated as
   `nation-only`. The pipeline must refuse to render restricted names on
   the public map.
4. **Per-name granularity.** Visibility is at the name level, not the
   Nation level. A Nation may share some names freely and keep others
   restricted; the type must support that.
5. **Provenance is required.** Every `LocalName` carries a `submitted_by`.
   Names without provenance are not loaded.
6. **No data without people.** This data structure does not get populated
   by botanists writing down what they think Indigenous names are. It gets
   populated by contributions from Nations and their representatives, or
   by explicitly-attributed published material with permissible licensing.
7. **The map renders local names alongside, never under, the binomial
   list.** The UI must not place Indigenous names as a sub-bullet of the
   Linnaean species.
8. **Right to withdraw.** A Nation may at any time ask that names they
   contributed be removed; the pipeline must support deletion (not just
   masking) of `LocalName` rows.

## When this gets implemented

Not in Phase 2. Phase 2 builds the map on VASCAN + GBIF + the 9 authored
species profiles, with sovereignty stubs at the Nation level. Local-name
data, if and when contributed, lands in Phase 4 (Collaboration & Launch)
or whenever a Nation is ready to bring it — whichever is later.

What Phase 2 does do: leave a clean shape for this work, so when a Nation
does engage, the conversation is "here is the model we propose, what would
you change?" rather than "we built it without you, fit your knowledge into
this box."
