# API reference draft for `factsage-compound`

This draft is organized around the public objects currently exported by the package.

## Module: `factsage-compound`

### Public classes

#### `Database(database_file)`
Load and parse a FactSage compound database from a binary `.CDB` file.

Key attributes:
- `database_file`: original file path
- `chunks`: raw chunk array loaded from disk
- `chunk_header`: parsed database header chunk
- `compounds`: parsed list of `Compound` objects

Key methods:
- `save()` — write in-memory chunks back to disk
- `find_compound_by_formula(formula)` — exact formula match
- `find_compound_by_name(name)` — prefix match on compound name
- `find_phase_by_chemapp_name(name)` — resolve ChemApp-style identifier to a phase

Internal parsing helpers:
- `_load()`
- `_parse()`
- `_parse_compound()`
- `_parse_compounds()`

#### `Compound(chunk, database)`
Wrap a compound chunk and link all associated phases, comments, and property ranges.

Key attributes:
- `chunk`
- `database`
- `phases`
- `comment_chunks`
- `name`
- `formula`
- `coefficients_real`

Key methods:
- `find_phase_by_name(name)`
- `find_phase_by_label_chemapp(label)`

Internal helpers:
- `_parse_phases()`
- `_parse_ranges()`
- `_parse_comments()`

#### `Phase(chunk, compound)`
Represent one phase of a compound.

Key attributes and properties:
- `chunk`
- `compound`
- `database`
- `ranges`
- `kappas`
- `name`
- `density`
- `state`
- `index`
- `label`
- `label_chemapp`

For non-transition phases:
- `enthalpy`
- `entropy`

For transition phases:
- `transition_enthalpy`
- `transition_temperature`

Key methods:
- `has_transition()`

Internal helper:
- `_load_cp_ranges()`

#### `Range(chunk, phase)`
Represent a heat-capacity range for a phase.

Key attributes and properties:
- `chunk`
- `phase`
- `database`
- `coefficients`
- `powers`
- `t_min`
- `t_max`
- `enthalpy`
- `entropy`

### Public functions

#### `parse_chemapp_name(name)`
Parse a ChemApp-style string into a dictionary with:
- `formula`
- `name`
- `label`

### Public constants

Chunk identifiers:
- `CHUNK_TYPE_DB`
- `CHUNK_TYPE_COMPOUND`
- `CHUNK_TYPE_PHASE1`
- `CHUNK_TYPE_PHASE2`
- `CHUNK_TYPE_CP1`
- `CHUNK_TYPE_CP2`
- `CHUNK_TYPE_CP3`
- `CHUNK_TYPE_CP4`
- `CHUNK_TYPE_CP5`
- `CHUNK_TYPE_COMMENT`
- `CHUNK_TYPE_KAPPA`

Binary dtype map:
- `DTYPES`

## Recommended pdoc command

```bash
PYTHONPATH=src pdoc -o docs factsage-compound
```

## Recommended docstring priorities

For the next pass, add docstrings to these public properties to improve generated docs:

- `Compound.name`
- `Compound.formula`
- `Compound.coefficients_real`
- `Phase.enthalpy`
- `Phase.entropy`
- `Phase.transition_enthalpy`
- `Phase.transition_temperature`
- `Phase.name`
- `Phase.density`
- `Phase.state`
- `Phase.index`
- `Phase.label`
- `Phase.label_chemapp`
- `Range.coefficients`
- `Range.powers`
- `Range.t_min`
- `Range.t_max`
- `Range.enthalpy`
- `Range.entropy`
