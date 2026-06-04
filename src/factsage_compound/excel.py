# excel.py
import xlwings as xw
import pandas as pd
from factsage_compound import compare

EXCEL_FUNCTION_GROUP = "FactSage Compound"

@xw.func(category=EXCEL_FUNCTION_GROUP)
@xw.arg('database', doc="")
@xw.arg('trigger', doc="")
@xw.ret(pd.DataFrame, index=False)
def factsage_list_compounds(database, trigger=None):
    """Returns a table containing information about compounds in a FactSage Compound database (XXXXBASE.cdb). This function can also be applied to the XXXXSOLN.fdb part of a FactSage Solution database in the new format (FactSage 7.0+) since the data formats are essentially identical.
    The following information is displayed:

    formula, name, phase, H298 [J/mol], S298 [J/mol/K], Ttrans [K], DtransH [J/mol], Tmin (range) [K], Tmax (range) [K], CP(coeff1), [J], CP(power1), ..., CP(coeff8), [J], CP(power8)

    Args:

    ***database*** an absolute or relative path to a FactSage Compound database.

    ***trigger***  an arbitrary value, does not affect the results, but triggers a function call each time when changed. Use each time when the compound database has been modified (via FactSage Compound module or another method) to get the most updated values.

    Returns:

    a table with the database content.

    """
    return compare.factsage_list_compounds(database, trigger)

@xw.func(category=EXCEL_FUNCTION_GROUP)
@xw.arg('database1', doc="")
@xw.arg('database2', doc="")
@xw.ret(pd.DataFrame, index=False)
def factsage_compare_compounds(database1, database2, trigger=None):
    """Returns a table comparing two different FactSage Compound databases (XXXXBASE.cdb). This function can also be applied to the XXXXSOLN.fdb part of a FactSage Solution database in the new format (FactSage 7.0+) since the data formats are essentially identical.
    The following information is displayed:
    formula_1, name_1, phase_1, H298_1 [J/mol], S298_1 [J/mol/K], Ttrans_1 [K], DtransH_1 [J/mol], Tmin_1 (range) [K], Tmax_1 (range) [K], CP(coeff1)_1, [J], CP(power1)_1, ..., CP(coeff8)_1, [J], CP(power8)_1
    formula_2, name_2, phase_2, H298_2 [J/mol], S298_2 [J/mol/K], Ttrans_2 [K], DtransH_2 [J/mol], Tmin_2 (range) [K], Tmax_2 (range) [K], CP(coeff1)_2, [J], CP(power1)_2, ..., CP(coeff8)_2, [J], CP(power8)_2

    Compounds only from the first database are displayed in the same order as they are entered in the database and the second half of the database shows if a compound from the first database is also present in the second one and what properties it has.
    Args:

    ***database1*** an absolute or relative path to the first FactSage Compound database.

    ***database2*** an absolute or relative path to the second FactSage Compound database.

    ***trigger***  an arbitrary value, does not affect the results, but triggers a function call each time when changed. Use each time when the compound database has been modified (via FactSage Compound module or another method) to get the most updated values.


    Returns:

    a table comparing two databases.
    """
    return compare.factsage_compare_compounds(database1, database2, trigger)