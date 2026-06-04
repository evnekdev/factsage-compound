"""Tools for reading and editing FactSage compound database (CDB) files.

The package parses the fixed-width binary chunk format used by FactSage
compound databases. Databases are loaded into a :class:`Database` object,
which exposes :class:`Compound`, :class:`Phase`, and :class:`Range` objects
for inspection and modification before saving the binary file back to disk.
"""

from factsage_compound.factsage_compound import Database
from factsage_compound.factsage_compound import Compound
from factsage_compound.factsage_compound import Phase
from factsage_compound.factsage_compound import Range

from factsage_compound.factsage_compound import parse_chemapp_name

from factsage_compound.factsage_compound import CHUNK_TYPE_DB
from factsage_compound.factsage_compound import CHUNK_TYPE_COMPOUND
from factsage_compound.factsage_compound import CHUNK_TYPE_PHASE1
from factsage_compound.factsage_compound import CHUNK_TYPE_PHASE2
from factsage_compound.factsage_compound import CHUNK_TYPE_CP1
from factsage_compound.factsage_compound import CHUNK_TYPE_CP2
from factsage_compound.factsage_compound import CHUNK_TYPE_CP3
from factsage_compound.factsage_compound import CHUNK_TYPE_CP4
from factsage_compound.factsage_compound import CHUNK_TYPE_CP5
from factsage_compound.factsage_compound import CHUNK_TYPE_COMMENT
from factsage_compound.factsage_compound import CHUNK_TYPE_KAPPA

from factsage_compound.factsage_compound import DTYPES
