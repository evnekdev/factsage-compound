import pyparsing as pp
import numpy as np
### Generic chunk, id + body
dbtype_chunk          = np.dtype([('chunk_id', np.uint8), # (0, 0)
                                  ('body', 'B', 255)
                                  ])

### Chunk body as the leading DB chunk (occurs only once in the beginning of the file)
dbtype_db_chunk       = np.dtype([('chunk_id', np.uint8), # (0, 0)
                                  ('padding1', 'B'),      # (0, 1)
                                  ('magic', 'S4'),        # (0, 2-6)
                                  ('padding2', 'B', 2),   # (0, 7-8)
                                  ('date', 'B', 8),
                                  ('read_flag', '?'),
                                  ('unknown1', 'B', 11),
                                  ('comment', 'S80'),
                                  ('padding3', 'B', 136),
                                  ('unknown2', 'B', 12)
                                  ])
                                  
### Repeated pattern across multiple chunks describing the same compound
dbtype_header         = np.dtype([('element_id', np.uint8, 7),     # row 0
                                  ('padding_coeff', 'B'),          # row 0
                                  ('element_coeff', np.uint8, 7),  # row 0
                                  ('charge_raw', np.int8),         # row 0
                                  ('entry_number', np.uint8),      # row 1
                                  ('reference', np.uint16, 2),     # row 1
                                  ('timestamp', 'B', 8),           # row 1
                                  ('unknown1', 'B',2)              # row 1
                                  ])                             #
                                  
### Compound chunk
dbtype_compound_chunk = np.dtype([('chunk_id', np.uint8),
                                  ('header', dbtype_header),
                                  ('compound_name', 'S40'),
                                  ('reserved_string1', 'S40'),
                                  ('formula_name', 'S40'),
                                  ('unknown', 'B', 4),
                                  ('unit_energy', np.uint32),
                                  ('unit_pressure', np.uint32),
                                  ('reserved_string2', 'S12'),
                                  ('coeff_real', np.float64, 7),
                                  ('padding_final', 'B', 24)
                                  ])
                                  
### Phase chunk of type I (H, S)
dbtype_phase_chunk_1 = np.dtype([('chunk_id', np.uint8),
                                 ('header', dbtype_header),
                                 ('enthalpy', np.float64),
                                 ('entropy', np.float64),
                                 ('phase_id_raw_neg', np.int32),
                                 ('phase_id_raw', np.int32),
                                 ('density_raw', np.float64),
                                 ('therm_expansion_coeff', np.float32, 4),
                                 ('compressibility_coeff', np.float32, 4),
                                 ('bulk_mod_derivative_coeff', np.float32, 2),
                                 ('temp_magn', np.float32),
                                 ('moment_magn', np.float32),
                                 ('pfactor', np.float32),
                                 ('padding1', 'B', 20),
                                 ('phase_name', 'S40'),
                                 ('padding2', 'B', 80)
                                 ])
                                 
### Phase chunk if type II (Htrans + Ttrans)
dbtype_phase_chunk_2 = np.dtype([('chunk_id', np.uint8),
                                 ('header', dbtype_header),
                                 ('enthalpy_trans', np.float64),
                                 ('temp_trans', np.float64),
                                 ('phase_id_raw_parent', np.int32),
                                 ('phase_id_raw', np.int32),
                                 ('density_raw', np.float64),
                                 ('therm_expansion_coeff', np.float32, 4),
                                 ('compressibility_coeff', np.float32, 4),
                                 ('bulk_mod_derivative_coeff', np.float32, 2),
                                 ('temp_magn', np.float32),
                                 ('moment_magn', np.float32),
                                 ('pfactor', np.float32),
                                 ('padding1', 'B', 20),
                                 ('phase_name', 'S40'),
                                 ('padding2', 'B', 80)
                                 ])
                                 
### CP range chunk (there are several ids corresponding to it, but I didn't find any significant different)
dbtype_cp_chunk      = np.dtype([('chunk_id', np.uint8),
                                ('header', dbtype_header),
                                ('enthalpy', np.float64),
                                ('entropy', np.float64),
                                ('phase_id_raw', np.int32),
                                ('unknown1', 'B', 4),
                                ('t_min', np.float64),
                                ('t_max', np.float64),
                                ('cp_coeff', np.float64, 8),
                                ('power', np.float64, 8),
                                ('padding_remaining', 'B', 56)
                                ])
                                
### Compound comment (in case it is long, comment chunks are stacked one after another)
dbtype_comment_chunk = np.dtype([('chunk_id', np.uint8),
                                 ('header', dbtype_header),
                                 ('comment', 'S80'),
                                 ('padding_remaining', 'B', 144)
                                 ])
                                 
### Extended physical properties chunk
dbtype_kappa_chunk   = np.dtype([('chunk_id', np.uint8),
                                 ('header', dbtype_header),
                                 ('t_min', np.float64),
                                 ('t_max', np.float64),
                                 ('phase_id_raw', np.int32),
                                 ('unknown1', 'B', 4),
                                 ('f1T_coeff', np.float64, 10),
                                 ('f1T_power', np.float32, 8),
                                 ('f2P_coeff', np.float64, 3),
                                 ('f2P_power', np.float32, 2),
                                 ('f3T_coeff', np.float64, 5),
                                 ('f3T_power', np.float32, 3),
                                 ('padding_remaining', 'B', 4)
                                 ])

pattern_chemapp_compound = pp.Word(pp.alphanums).setResultsName('formula') \
                           + pp.Literal('_').suppress() \
                           + pp.Group(pp.Word(pp.alphanums + '_') \
                           + pp.Optional('(') \
                           + pp.Optional(pp.Word(pp.alphanums)) \
                           + pp.Optional(')')).setResultsName('name').setParseAction(lambda s, loc, toks: ''.join(toks[0])) \
                           + pp.Literal('(').suppress() \
                           + pp.Group(pp.Literal('s')|pp.Literal('l')|pp.Literal('g')|pp.Literal('aq')).setResultsName('state', listAllMatches=False).setParseAction(lambda s, loc, toks: toks[0][0]) \
                           + pp.Word(pp.nums).setResultsName('index') \
                           + pp.Literal(')').suppress()


"""
CHUNK_TYPE_DB = b'x\09'
CHUNK_TYPE_COMPOUND = b'x\01'
CHUNK_TYPE_PHASE1 = b'x\07'
CHUNK_TYPE_PHASE2 = b'x\08'
CHUNK_TYPE_CP1 = b'x\02'
CHUNK_TYPE_CP2 = b'x\04'
CHUNK_TYPE_CP3 = b'x\05'
CHUNK_TYPE_CP4 = b'x\03'
CHUNK_TYPE_COMMENT = b'x\10'
CHUNK_TYPE_PHYSPROP = b'x\11'
"""
### Binary u8 representations
CHUNK_TYPE_DB = 9
CHUNK_TYPE_COMPOUND = 1
CHUNK_TYPE_PHASE1 = 7
CHUNK_TYPE_PHASE2 = 8
CHUNK_TYPE_CP1 = 2
CHUNK_TYPE_CP2 = 4
CHUNK_TYPE_CP3 = 5
CHUNK_TYPE_CP4 = 3
CHUNK_TYPE_CP5 = 6
CHUNK_TYPE_COMMENT = 10
CHUNK_TYPE_KAPPA = 11

DTYPES = {CHUNK_TYPE_DB:       dbtype_db_chunk,
          CHUNK_TYPE_COMPOUND: dbtype_compound_chunk,
          CHUNK_TYPE_PHASE1:   dbtype_phase_chunk_1,
          CHUNK_TYPE_PHASE2:   dbtype_phase_chunk_2,
          CHUNK_TYPE_CP1:      dbtype_cp_chunk,
          CHUNK_TYPE_CP2:      dbtype_cp_chunk,
          CHUNK_TYPE_CP3:      dbtype_cp_chunk,
          CHUNK_TYPE_CP4:      dbtype_cp_chunk,
          CHUNK_TYPE_CP5:      dbtype_cp_chunk,
          CHUNK_TYPE_COMMENT:  dbtype_comment_chunk,
          CHUNK_TYPE_KAPPA:    dbtype_kappa_chunk
          }

def parse_chemapp_name(name):
    """Split a ChemApp-style identifier into formula, name, and phase label.

    Parameters
    ----------
    name : str
        Identifier such as ``FeO_wustite(s)`` or a similarly formatted string.

    Returns
    -------
    dict
        Dictionary with ``formula``, ``name``, and ``label`` keys.
    """
    name = str(name)
    index1 = 0
    index2 = len(name)-1
    for k in range(0, len(name)):
        if name[k] == '_':
            break
        index1 += 1
    for k in range(len(name)-1, 0,-1):
        if name[k] == '(':
            break
        index2 -= 1
    return {"formula": name[0:index1], "name": name[index1+1:index2], "label": name[index2+1:-1]}


class Database:
    """Represent a loaded FactSage compound database.

    Parameters
    ----------
    database_file : str or path-like
        Path to the binary ``.CDB`` file.
    """

    def __init__(self, database_file):
        """Load and parse the database file into Python objects."""
        self.database_file = database_file
        self.compounds = []
        self._load()
        self._parse()

    def _load(self):
        """Read the raw 256-byte chunks from disk into a writable NumPy array."""
        with open(self.database_file, 'rb') as fh:
            self.chunks = np.frombuffer(fh.read(), dtype=dbtype_chunk).copy() # the original byte array, created by fh.read(), is immutable and cannot be modified, so we are creating a copy
            self.chunks.setflags(write=1)

    def _parse(self):
        """Parse the database header and all compound records."""
        self.chunk_header = self.chunks[0].view(dtype=dbtype_db_chunk)
        self.cursor = 1
        while self.cursor < self.chunks.shape[0]:
            self._parse_compound()

    def _parse_compound(self):
        """Parse the compound at the current cursor position."""
        if self.chunks[self.cursor]['chunk_id'] != CHUNK_TYPE_COMPOUND:
            raise Exception(f"Unable to parse block {self.cursor}, supposed to find a COMPOUND block, block id = {self.chunks[self.cursor]['chunk_id']}")
        chunk = self.chunks[self.cursor].view(dtype=dbtype_compound_chunk)
        self.cursor += 1
        compound = Compound(chunk, self)
        self.compounds.append(compound)


    def _parse_compounds(self):
        for k in range(0, self.chunks.shape[0]):
            if self.chunks[k]['chunk_id'] == CHUNK_TYPE_COMPOUND:
                chunk =self.chunks[k].view(dtype=dbtype_compound_chunk)
                self.cursor += 1
                self.compounds.append(Compound(chunk, self))

    def save(self):
        """Write the current in-memory chunk array back to the source file."""
        with open(self.database_file, 'wb') as fh:
            fh.write(self.chunks)

    def find_compound_by_formula(self, formula):
        """Return the first compound whose formula exactly matches ``formula``."""
        for cmp in self.compounds:
            if cmp.formula == formula:
                return cmp
        return None

    def find_compound_by_name(self, name):
        """Return the first compound whose name starts with ``name``."""
        for cmp in self.compounds:
            if cmp.name.startswith(name):
                return cmp
        return None

    def find_phase_by_chemapp_name(self, name):
        """Find a phase from a ChemApp-style identifier string."""
        res = parse_chemapp_name(name)
        cmp = self.find_compound_by_formula(res['formula'])
        if cmp is not None:
            return cmp.find_phase_by_label_chemapp(res['label'])
        return None


class Compound:
    """Represent a compound record and its associated phases and comments."""
    def __init__(self, chunk, database):
        """Create a compound wrapper around a parsed binary chunk."""
        self.chunk = chunk
        self.database = database
        self.phases = []
        self.comment_chunks = []
        self._parse_phases()
        self._parse_ranges()
        self._parse_comments()

    def _parse_phases(self):
        """Parse consecutive phase chunks belonging to this compound."""
        for k in range(self.database.cursor, self.database.chunks.shape[0]):
            if self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_PHASE1:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_phase_chunk_1)
            elif self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_PHASE2:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_phase_chunk_2)
            else:
                return
            self.database.cursor += 1
            phase = Phase(chunk, self)
            self.phases.append(phase)

    def _parse_ranges(self):
        """Attach heat-capacity and kappa chunks to their owning phases."""
        for k in range(self.database.cursor, self.database.chunks.shape[0]):
            if self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_CP1:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_CP2:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_CP3:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_CP4:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_CP5:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_KAPPA:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_kappa_chunk)
            else:
                return
            self.database.cursor += 1
            phase_id_raw = chunk['phase_id_raw']
            for k in range(0, len(self.phases)):
                phase = self.phases[k]
                if phase.chunk['phase_id_raw'] == phase_id_raw:
                    if chunk['chunk_id'] == CHUNK_TYPE_KAPPA:
                        phase.kappas.append(chunk) # TODO
                    else:
                        phase.ranges.append(Range(chunk, phase))

    def _parse_comments(self):
        """Collect stacked comment chunks for the current compound."""
        for k in range(self.database.cursor, self.database.chunks.shape[0]):
            if self.database.chunks[self.database.cursor]['chunk_id'] == CHUNK_TYPE_COMMENT:
                chunk = self.database.chunks[self.database.cursor].view(dtype=dbtype_comment_chunk)
            else:
                return
            self.database.cursor += 1
            self.comment_chunks.append(chunk)


    @property
    def name(self):
        return self.chunk['compound_name'].decode('ascii').strip()

    @name.setter
    def name(self, value):
        if len(value) > 40:
            raise Exception("Compound names cannot exceed 40 characters.")
        self.chunk['compound_name'] = value.encode()

    @property
    def formula(self):
        return self.chunk['formula_name'].decode('ascii').strip()

    @property
    def coefficients_real(self):
        return self.chunk['coeff_real']

    @coefficients_real.setter
    def coefficients_real(self, value):
        if value.shape[0] > 7:
            raise Exception("Only up to 7 elements are allowed.")
        self.chunk['coeff_real'][0:value.shape[0]] = value

    def __str__(self):
        if self.name == "":
            return f"{self.formula}"
        return f"{self.formula} ({self.name})"

    def __repr__(self):
        return self.__str__()

    def find_phase_by_name(self, name):
        """Return the first phase whose display name exactly matches ``name``."""
        for phase in self.phases:
            if phase.name == name:
                return phase
        return None

    def find_phase_by_label_chemapp(self, label):
        """Return the first phase whose ChemApp label matches ``label``."""
        for phase in self.phases:
            if phase.label_chemapp == label:
                return phase
        return None


class Phase:
    """Represent one thermodynamic phase for a compound."""
    def __init__(self, chunk, compound):
        """Create a phase wrapper and prepare linked ranges and kappas."""
        self.chunk = chunk
        self.compound = compound
        self.database = compound.database
        self.ranges = []
        self.kappas = []

    def _load_cp_ranges(self):
        elements = self.chunk['header']['element_id']
        coeffs = self.chunk['header']['element_coeff']
        charge_raw = self.chunk['header']['charge_raw']
        phase_id_raw = self.chunk['phase_id_raw']
        for k in range(0, self.database.chunks.shape[0]):
            if self.database.chunks[k]['chunk_id'] == CHUNK_TYPE_CP1:
                chunk = self.database.chunks[k].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[k]['chunk_id'] == CHUNK_TYPE_CP2:
                chunk = self.database.chunks[k].view(dtype=dbtype_cp_chunk)
            elif self.database.chunks[k]['chunk_id'] == CHUNK_TYPE_CP3:
                chunk = self.database.chunks[k].view(dtype=dbtype_cp_chunk)
            else:
                continue
            if (chunk['phase_id_raw'] == phase_id_raw) and np.array_equal(chunk['header']['element_id'], elements) and np.array_equal(chunk['header']['element_coeff'], coeffs) and (chunk['header']['charge_raw'] == charge_raw):
                self.ranges.append(Range(chunk, self))

    def has_transition(self):
        """Return ``True`` when the phase is encoded as a transition phase."""
        return self.chunk['chunk_id'] == CHUNK_TYPE_PHASE2

    @property
    def enthalpy(self):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE1:
            value = self.chunk['enthalpy']
            if self.compound.chunk['unit_energy'] == 0:
                value *= 4.184
            return value
        else:
            raise Exception("Not supported if a transition is defined")

    @enthalpy.setter
    def enthalpy(self, value):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE1:
            if self.compound.chunk['unit_energy'] == 0:
                value /= 4.184
            self.chunk['enthalpy'] = value
            for range in self.ranges:
                range.enthalpy = value
        else:
            raise Exception("Not supported if a transition is defined")

    @property
    def entropy(self):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE1:
            value = self.chunk['entropy']
            if self.compound.chunk['unit_energy'] == 0:
                value *= 4.184
            return value
        else:
            raise Exception("Not supported if a transition is defined")

    @entropy.setter
    def entropy(self, value):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE1:
            if self.compound.chunk['unit_energy'] == 0:
                value /= 4.184
            self.chunk['entropy'] = value
            for range in self.ranges:
                range.entropy = value
        else:
            raise Exception("Not supported if a transition is defined")

    @property
    def transition_enthalpy(self):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE2:
            value = self.chunk['enthalpy_trans']
            if self.compound.chunk['unit_energy'] == 0:
                value *= 4.184
            return value
        else:
            raise Exception("Not supported without a transition")

    @transition_enthalpy.setter
    def transition_enthalpy(self, value):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE2:
            value /= 4.184
            self.chunk['enthalpy_trans'] = value
            #TODO change ranges
        else:
            raise Exception("Not supported without a transition")

    @property
    def transition_temperature(self):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE2:
            value = self.chunk['temp_trans']
            return value
        else:
            raise Exception("Not supported without a transition")

    @transition_temperature.setter
    def transition_temperature(self, value):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE2:
            self.chunk['temp_trans'] = value
        else:
            raise Exception("Not supported without a transition")

    @property
    def name(self):
        return self.chunk['phase_name'].decode('ascii').strip()

    @name.setter
    def name(self, value):
        if len(value) > 40:
            raise Exception("Names with more than 40 characters are not supported")
        self.chunk['phase_name'] = value.encode('ascii')

    @property
    def density(self):
        return self.chunk['density_raw'] % 1000000

    @density.setter
    def density(self, value):
        self.chunk['density_raw'] = int(self.chunk['density_raw'] / 1000000) * 1000000 + value

    def __str__(self):
        if self.chunk['chunk_id'] == CHUNK_TYPE_PHASE1:
            return f"{self.name}, H298={self.enthalpy:0.3f} J/mol, S298={self.entropy:0.3f} J/mol/K"
        else:
            return f"{self.name}, DtransH={self.transition_enthalpy:0.3f} J/mol, Ttrans={self.transition_temperature:.2f} K"

    def __repr__(self):
        return self.__str__()

    @property
    def state(self):
        id_raw = self.chunk['phase_id_raw']
        if id_raw > 990:
            return 'Aq'
        if id_raw > 900:
            return 'G'
        if id_raw > 800:
            return 'L'
        return 'S'

    @property
    def index(self):
        id_raw = self.chunk['phase_id_raw']
        if id_raw > 990:
            return id_raw - 990
        if id_raw > 900:
            return id_raw - 900
        if id_raw > 800:
            return id_raw - 800
        return id_raw - 100

    @property
    def label(self):
        return f"{self.state}{self.index}"

    @property
    def label_chemapp(self):
        state = self.state
        index = self.index
        if index == 1:
            return f"{self.state.lower()}"
        return f"{self.state.lower()}{self.index}"





class Range:
    """Represent a heat-capacity coefficient range for a phase."""
    def __init__(self, chunk, phase):
        """Wrap a parsed heat-capacity chunk for a phase."""
        self.chunk = chunk
        self.phase = phase
        self.database = phase.database

    @property
    def coefficients(self):
        return self.chunk['cp_coeff']

    @property
    def powers(self):
        return self.chunk['power']

    @property
    def t_min(self):
        return self.chunk['t_min']

    @property
    def t_max(self):
        return self.chunk['t_max']

    @property
    def enthalpy(self):
        return self.chunk['enthalpy']

    @enthalpy.setter
    def enthalpy(self, value):
        self.chunk['enthalpy'] = value

    @property
    def entropy(self):
        return self.chunk['entropy']

    @entropy.setter
    def entropy(self, value):
        self.chunk['entropy'] = value

    def __str__(self):
        coeffs = self.coefficients
        powers  =self.powers
        return f"{self.t_min:0.3f}-{self.t_max:0.3f}K, {coeffs[0]}*T^{powers[0]:0.2f}+{coeffs[1]}*T^{powers[1]:0.2f}+{coeffs[2]}*T^{powers[2]:0.2f}+{coeffs[3]}*T^{powers[3]:0.2f}+{coeffs[4]}*T^{powers[4]:0.2f}+{coeffs[5]}*T^{powers[5]:0.2f}+{coeffs[6]}*T^{powers[6]:0.2f}+{coeffs[7]}*T^{powers[7]:0.2f}, H = {self.enthalpy}, S = {self.entropy}"

    def __repr__(self):
        return self.__str__()

