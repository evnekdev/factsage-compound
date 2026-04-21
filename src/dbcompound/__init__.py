"""Tools for reading and editing FactSage compound database (CDB) files.

The package parses the fixed-width binary chunk format used by FactSage
compound databases. Databases are loaded into a :class:`Database` object,
which exposes :class:`Compound`, :class:`Phase`, and :class:`Range` objects
for inspection and modification before saving the binary file back to disk.
"""

from dbcompound.dbcompound import Database
from dbcompound.dbcompound import Compound
from dbcompound.dbcompound import Phase
from dbcompound.dbcompound import Range

from dbcompound.dbcompound import parse_chemapp_name

from dbcompound.dbcompound import CHUNK_TYPE_DB
from dbcompound.dbcompound import CHUNK_TYPE_COMPOUND
from dbcompound.dbcompound import CHUNK_TYPE_PHASE1
from dbcompound.dbcompound import CHUNK_TYPE_PHASE2
from dbcompound.dbcompound import CHUNK_TYPE_CP1
from dbcompound.dbcompound import CHUNK_TYPE_CP2
from dbcompound.dbcompound import CHUNK_TYPE_CP3
from dbcompound.dbcompound import CHUNK_TYPE_CP4
from dbcompound.dbcompound import CHUNK_TYPE_CP5
from dbcompound.dbcompound import CHUNK_TYPE_COMMENT
from dbcompound.dbcompound import CHUNK_TYPE_KAPPA

from dbcompound.dbcompound import DTYPES
