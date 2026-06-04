# factsage-compound

`factsage-compound` is a Python package for reading, inspecting, and editing FactSage Compound Database (`.CDB`) files.

It parses the fixed-width binary chunk format used by FactSage compound databases and exposes Python objects for:

- loading a database into memory
- iterating through compounds and phases
- inspecting thermodynamic values and heat-capacity ranges
- editing selected values in memory
- saving the modified binary back to disk

## Wiki project for Compound Database files (not part of the official FactSage distribution, written by Dr Evgenii Nekhoroshev)

The detailed documentation on the internal workings of the FactSage Compound Database file format is located at:

[FactSage Compound Database Project](https://evnekdev.github.io/factsage-compound-docs/)

## Features

- Parses FactSage compound database chunks into structured NumPy-backed objects
- Provides object wrappers for `Database`, `Compound`, `Phase`, and `Range`
- Supports lookup by formula, compound name, and ChemApp-style phase labels
- Preserves binary layout so modified databases can be written back to disk

## Requirements

- Python 3.9 to 3.11
- `numpy==1.23.*`
- `pyparsing==3.1.*`

## Installation

From a local checkout:

```bash
pip install .
```

Or install dependencies manually for development:

```bash
pip install numpy==1.23.* pyparsing==3.1.*
```

## Quick start (Excel interface, database comparison)

To use database comparison functions from Excel, you need to install xlwings using :

```cmd
pip install xlwings
```

Then locate the `xlwings` addin in `$PYTHONPATH\Lib\site-packages\xlwings\addin` through Excel File -> Options -> Add-ins (Manage Excel Addins, Go) interface. If everything goes ok, an `xlwings` tab appears in the top Excel Ribbon.

In File -> Options -> Trust Center -> Trust Center Settings -> Macro Settings set "Enable VBA macros" toggle button and "Enable Excel 4.0 macros when VBA macros are enabled" and "Trust access to the VBA project object model" ticks.

You can download an xlsm templates from [Excel Template](examples/Template.xlsm).

If you create your own xlsm book from scratch, you will need an xlwings.conf sheet with the following contents:

| | A | B |
|---|---|---|
|1| Interpreter_Win | $PYTHONPATH\python.exe |
|2| Interpreter_Mac |                        |
|3| PYTHONPATH      |                        |
|4| Conda Path      |                        |
|5| Conda Env       |                        |
|6| UDF Modules     | factsage-compound      |
|7| Debug UDFs      | FALSE                  |
|8| Use UDF Server  | TRUE                   |
|9| Show Console    | TRUE                   |


## Quick start (pure Python)

```python
from factsage_compound import Database

# Load an existing FactSage compound database
db = Database("SENDBASE.CDB")

print(f"Compounds: {len(db.compounds)}")

# Find a compound and inspect its phases
compound = db.find_compound_by_formula("FeO")
if compound is not None:
    print(compound.name)
    for phase in compound.phases:
        print(phase.label, phase.name)
```

## Data model

### Database

`Database` loads the binary `.CDB` file and parses it into a list of `Compound` objects.

Useful methods:

- `save()` writes the current in-memory chunk array back to the original file
- `find_compound_by_formula(formula)` returns the first matching compound
- `find_compound_by_name(name)` returns the first compound whose name starts with the provided text
- `find_phase_by_chemapp_name(name)` resolves a ChemApp-style identifier and returns the matching phase

### Compound

`Compound` wraps a compound chunk and collects associated phases, heat-capacity ranges, and comments.

Useful attributes and methods:

- `name`: human-readable compound name
- `formula`: formula string stored in the file
- `coefficients_real`: real stoichiometric coefficients array
- `phases`: list of `Phase` instances
- `find_phase_by_name(name)`
- `find_phase_by_label_chemapp(label)`

### Phase

`Phase` represents one thermodynamic phase of a compound.

Useful attributes:

- `name`
- `density`
- `state` (`S`, `L`, `G`, or `Aq`)
- `index`
- `label`
- `label_chemapp`
- `ranges`
- `kappas`

For non-transition phases (`chunk_id == CHUNK_TYPE_PHASE1`):

- `enthalpy`
- `entropy`

For transition phases (`chunk_id == CHUNK_TYPE_PHASE2`):

- `transition_enthalpy`
- `transition_temperature`

### Range

`Range` stores heat-capacity coefficients for a temperature interval.

Useful attributes:

- `coefficients`
- `powers`
- `t_min`
- `t_max`
- `enthalpy`
- `entropy`

## Example workflows

### Find a phase by ChemApp label

```python
from factsage_compound import Database

db = Database("SENDBASE.CDB")
phase = db.find_phase_by_chemapp_name("FeO_wustite(s)")

if phase:
    print(phase.name)
    print(phase.label_chemapp)
```

### Update thermodynamic values and save

```python
from factsage_compound import Database

db = Database("SENDBASE.CDB")
compound = db.find_compound_by_formula("FeO")
phase = compound.find_phase_by_name("Wustite")

if phase and not phase.has_transition():
    phase.enthalpy = phase.enthalpy + 100.0
    phase.entropy = phase.entropy + 0.1

 db.save()
```

## Generating API docs with pdoc

The package is a good fit for `pdoc`, especially after adding proper module, class, and method docstrings.

Install pdoc:

```bash
pip install pdoc
```

Generate HTML docs:

```bash
PYTHONPATH=src pdoc -o docs dbcompound
```

Serve locally:

```bash
PYTHONPATH=src pdoc -p 8000 dbcompound
```

## Notes and caveats

- The parser assumes the fixed-width 256-byte chunk layout used by FactSage CDB files.
- Saving writes back to the original file path, so keep a backup of the source `.CDB` file.
- Several low-level constants and NumPy dtypes are public, but most users will work through the object wrappers.
- Some debug-style prints and TODO comments still exist in the code and may be worth cleaning up before a public release.

## Suggested next improvements

- Add docstrings to every public property for richer generated docs
- Add type hints for public methods and return values
- Replace generic `Exception` raises with more specific exception types
- Add tests using small fixture databases
- Add packaging metadata such as a license and project URLs
