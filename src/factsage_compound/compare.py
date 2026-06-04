# compare.py

import xlwings as xw
import pandas as pd
import numpy as np

def factsage_list_compounds(database, trigger=None):
    database = cmp.Database(database)
    output = _attributes_empty()
    for compound in database.compounds:
        output_ = _attributes_compound(compound)
        for key in output:
            output[key] += output_[key]
    df = pd.DataFrame({'formula': output['formulas'], 'name': output['names'], 'phase': output['phases'], 'H298': output['enthalpies'], 'S298': output['entropies'],
                       'enthalpy of transition': output['enthalpies_trans'], 'transition temperature': output['temp_trans'], 'T(range) min, K': output['temp_min'],
                       'T(range) max, K': output['temp_max'], 'CP(val)[1]': output['cp_coeff0'], 'CP(pow)[1]': output['cp_power0'], 'CP(val)[2]': output['cp_coeff1'],
                       'CP(pow)[2]': output['cp_power1'], 'CP(val)[3]': output['cp_coeff2'], 'CP(pow)[3]': output['cp_power2'], 'CP(val)[4]': output['cp_coeff3'],
                       'CP(pow)[4]': output['cp_power3'], 'CP(val)[5]': output['cp_coeff4'], 'CP(pow)[5]': output['cp_power4'], 'CP(val)[6]': output['cp_coeff5'],
                       'CP(pow)[6]': output['cp_power5'], 'CP(val)[7]': output['cp_coeff6'], 'CP(pow)[7]': output['cp_power6'], 'CP(val)[8]': output['cp_coeff7'],
                       'CP(pow)[8]': output['cp_power7']})
    #df = pd.DataFrame({'formula': formulas_0, 'name': names_0, 'phase': phases_0})
    return df

def factsage_compare_compounds(database1, database2, trigger=None):
    database1 = cmp.Database(database1)
    database2 = cmp.Database(database2)
    output1 = _attributes_empty()
    output2 = _attributes_empty()
    formulas1 = [compound.formula for compound in database1.compounds]
    formulas2 = [compound.formula for compound in database2.compounds]
    formulas = formulas1 + list(set(formulas1)-set(formulas2))
    for formula in formulas:
        if formula in formulas1:
            compound1 = database1.find_compound_by_formula(formula)
        else:
            compound1 = None
        if formula in formulas2:
            compound2 = database2.find_compound_by_formula(formula)
        else:
            compound2 = None
        output1_, output2_ = _attribute_compare_compounds(compound1, compound2)
        for key in output1:
            output1[key] += output1_[key]
        for key in output2:
            output2[key] += output2_[key]
    df = pd.DataFrame({'formula_1': output1['formulas'], 'name_1': output1['names'], 'phase_1': output1['phases'],
                       'H298_1': output1['enthalpies'], 'S298_1': output1['entropies'], 'Ttrans_1': output1['temp_trans'], 'Htrans_1': output1['enthalpies_trans'],
                       'T(range) min, K, 1': output1['temp_min'], 'T(range) max K, 1': output1['temp_max'],
                       'CP(val1)_1': output1['cp_coeff0'], 'CP(pow1)_1': output1['cp_power0'], 'CP(val2)_1': output1['cp_coeff1'], 'CP(pow2)_1': output1['cp_power1'],
                       'CP(val3)_1': output1['cp_coeff2'], 'CP(pow3)_1': output1['cp_power2'], 'CP(val4)_1': output1['cp_coeff3'], 'CP(pow4)_1': output1['cp_power3'],
                       'CP(val5)_1': output1['cp_coeff4'], 'CP(pow5)_1': output1['cp_power4'], 'CP(val6)_1': output1['cp_coeff5'], 'CP(pow6)_1': output1['cp_power5'],
                       'CP(val7)_1': output1['cp_coeff6'], 'CP(pow7)_1': output1['cp_power6'], 'CP(val8)_1': output1['cp_coeff7'], 'CP(pow8)_1': output1['cp_power7'],
                       'formula_2': output2['formulas'], 'name_2': output2['names'], 'phase_2': output2['phases'],
                       'H298_2': output2['enthalpies'], 'S298_2': output2['entropies'], 'Ttrans_2': output2['temp_trans'], 'Htrans_2': output2['enthalpies_trans'],
                       'T(range) min, K, 2': output2['temp_min'], 'T(range) max K, 2': output2['temp_max'],
                       'CP(val1)_2': output2['cp_coeff0'], 'CP(pow1)_2': output2['cp_power0'], 'CP(val2)_2': output2['cp_coeff1'], 'CP(pow2)_2': output2['cp_power1'],
                       'CP(val3)_2': output2['cp_coeff2'], 'CP(pow3)_2': output2['cp_power2'], 'CP(val4)_2': output2['cp_coeff3'], 'CP(pow4)_2': output2['cp_power3'],
                       'CP(val5)_2': output2['cp_coeff4'], 'CP(pow5)_2': output2['cp_power4'], 'CP(val6)_2': output2['cp_coeff5'], 'CP(pow6)_2': output2['cp_power5'],
                       'CP(val7)_2': output2['cp_coeff6'], 'CP(pow7)_2': output2['cp_power6'], 'CP(val8)_2': output2['cp_coeff7'], 'CP(pow8)_2': output2['cp_power7']})
    return df

def _attributes_empty():
    output = {}
    output['names'] = []
    output['formulas'] = []
    output['phases'] = []
    output['enthalpies'] = []
    output['entropies'] = []
    output['enthalpies_trans'] = []
    output['temp_trans'] = []
    output['temp_max'] = []
    output['temp_min'] = []
    output['cp_coeff0'] = []
    output['cp_coeff1'] = []
    output['cp_coeff2'] = []
    output['cp_coeff3'] = []
    output['cp_coeff4'] = []
    output['cp_coeff5'] = []
    output['cp_coeff6'] = []
    output['cp_coeff7'] = []
    output['cp_power0'] = []
    output['cp_power1'] = []
    output['cp_power2'] = []
    output['cp_power3'] = []
    output['cp_power4'] = []
    output['cp_power5'] = []
    output['cp_power6'] = []
    output['cp_power7'] = []
    return output

def _attributes_range(range):
    phase = range.phase
    compound = phase.compound
    output = _attributes_empty()
    output['names'].append(compound.name)
    output['formulas'].append(compound.formula)
    output['phases'].append(phase.name)
    if phase.has_transition():
        output['enthalpies'].append(np.nan)
        output['entropies'].append(np.nan)
        output['enthalpies_trans'].append(phase.transition_enthalpy)
        output['temp_trans'].append(phase.transition_temperature)
    else:
        output['enthalpies'].append(phase.enthalpy)
        output['entropies'].append(phase.entropy)
        output['temp_trans'].append(np.nan)
        output['enthalpies_trans'].append(np.nan)
    output['temp_min'].append(range.t_min)
    output['temp_max'].append(range.t_max)
    output['cp_coeff0'].append(range.coefficients[0])
    output['cp_coeff1'].append(range.coefficients[1])
    output['cp_coeff2'].append(range.coefficients[2])
    output['cp_coeff3'].append(range.coefficients[3])
    output['cp_coeff4'].append(range.coefficients[4])
    output['cp_coeff5'].append(range.coefficients[5])
    output['cp_coeff6'].append(range.coefficients[6])
    output['cp_coeff7'].append(range.coefficients[7])
    output['cp_power0'].append(range.powers[0])
    output['cp_power1'].append(range.powers[1])
    output['cp_power2'].append(range.powers[2])
    output['cp_power3'].append(range.powers[3])
    output['cp_power4'].append(range.powers[4])
    output['cp_power5'].append(range.powers[5])
    output['cp_power6'].append(range.powers[6])
    output['cp_power7'].append(range.powers[7])
    return output

def _attributes_phase(phase):
    compound = phase.compound
    output = _attributes_empty()
    for range in phase.ranges:
        output_ = _attributes_range(range)
        for key in output:
            output[key] += output_[key]
    return output

def _attributes_compound(compound):
    output = _attributes_empty()
    for phase in compound.phases:
        output_ = _attributes_phase(phase)
        for key in output:
            output[key] += output_[key]
    return output

def factsage_list_compounds(database, trigger=None):
    database = cmp.Database(database)
    output = _attributes_empty()
    for compound in database.compounds:
        output_ = _attributes_compound(compound)
        for key in output:
            output[key] += output_[key]
    df = pd.DataFrame({'formula': output['formulas'], 'name': output['names'], 'phase': output['phases'], 'H298': output['enthalpies'], 'S298': output['entropies'],
                       'enthalpy of transition': output['enthalpies_trans'], 'transition temperature': output['temp_trans'], 'T(range) min, K': output['temp_min'],
                       'T(range) max, K': output['temp_max'], 'CP(val)[1]': output['cp_coeff0'], 'CP(pow)[1]': output['cp_power0'], 'CP(val)[2]': output['cp_coeff1'],
                       'CP(pow)[2]': output['cp_power1'], 'CP(val)[3]': output['cp_coeff2'], 'CP(pow)[3]': output['cp_power2'], 'CP(val)[4]': output['cp_coeff3'],
                       'CP(pow)[4]': output['cp_power3'], 'CP(val)[5]': output['cp_coeff4'], 'CP(pow)[5]': output['cp_power4'], 'CP(val)[6]': output['cp_coeff5'],
                       'CP(pow)[6]': output['cp_power5'], 'CP(val)[7]': output['cp_coeff6'], 'CP(pow)[7]': output['cp_power6'], 'CP(val)[8]': output['cp_coeff7'],
                       'CP(pow)[8]': output['cp_power7']})
    #df = pd.DataFrame({'formula': formulas_0, 'name': names_0, 'phase': phases_0})
    return df

def _fill_with_nans(input):
    output = {}
    for key in input:
        vals = input[key]
        vals_nan = [np.nan]*len(vals)
        output[key] = vals_nan
    return output

def _attribute_compare_ranges(range1, range2):
    #print(f"range1 = {range1}")
    #print(f"range2 = {range2}")
    output1 = _attributes_empty()
    output2 = _attributes_empty()
    if range1 is not None:
        output1 = _attributes_range(range1)
    if range2 is not None:
        output2 = _attributes_range(range2)
        #print(f"output2 = {output2}")
    if range1 is None:
        output1 = _fill_with_nans(output2)
    if range2 is None:
        output2 = _fill_with_nans(output1)
    #print(f"output1 = {output1}")
    #print(f"output2 = {output2}")
    return output1, output2

def _attribute_compare_phases(phase1, phase2):
    #print(f"{phase1.ranges}")
    #print(f"{phase2.ranges}")
    output1 = _attributes_empty()
    output2 = _attributes_empty()
    if phase1 is None:
        for rng in phase2.ranges:
            output1_, output2_ = _attribute_compare_ranges(None, rng)
            for key in output1:
                output1[key] += output1_[key]
            for key in output2:
                output2[key] += output2_[key]
        return output1, output2
    if phase2 is None:
        for rng in phase1.ranges:
            output1_, output2_ = _attribute_compare_ranges(rng, None)
            for key in output1:
                output1[key] += output1_[key]
            for key in output2:
                output2[key] += output2_[key]
        return output1, output2
    nranges1 = len(phase1.ranges)
    nranges2 = len(phase2.ranges)
    nmin = min(nranges1, nranges2)
    nmax = max(nranges1, nranges2)
    for k in range(0, nmin):
        #print(f"{phase1.ranges[k]}")
        #print(f"{phase2.ranges[k]}")
        output1_, output2_ = _attribute_compare_ranges(phase1.ranges[k], phase2.ranges[k])
        for key in output1:
            output1[key] += output1_[key]
        for key in output2:
            output2[key] += output2_[key]
    for k in range(0, nmax-nmin):
        if nmax > nranges1:
            output1_, output2_ = _attribute_compare_ranges(None, phase2.ranges[nmin+k])
        else:
            output1_, output2_ = _attribute_compare_ranges(phase1.ranges[nmin+k], None)
        #print(f"output1_ = {output1_}")
        #print(f"output2_ = {output2_}")
        for key in output1:
            #print(f"output1[key] = {output1[key]}")
            #print(f"output1_[key] = {output1_[key]}")
            output1[key] += output1_[key]
        for key in output2:
            output2[key] += output2_[key]
    return output1, output2

def _attribute_compare_compounds(compound1, compound2):
    output1 = _attributes_empty()
    output2 = _attributes_empty()
    if compound1 is None:
        for phase in compound2.phases:
            output1_, output2_ = _attribute_compare_phases(None, phase)
            for key in output1:
                output1[key] += output1_[key]
            for key in output2:
                output2[key] += output2_[key]
        return output1, output2
    if compound2 is None:
        for phase in compound1.phases:
            output1_, output2_ = _attribute_compare_phases(phase, None)
            for key in output1:
                output1[key] += output1_[key]
            for key in output2:
                output2[key] += output2_[key]
        return output1, output2
    phases1 = [phase.name for phase in compound1.phases]
    phases2 = [phase.name for phase in compound2.phases]
    phases = phases1 + list(set(phases1)-set(phases2))
    for phase in phases:
        if phase in phases1:
            phase1_ = compound1.find_phase_by_name(phase)
        else:
            phase1_ = None
        if phase in phases2:
            phase2_ = compound2.find_phase_by_name(phase)
        else:
            phase2_ = None
        output1_, output2_ = _attribute_compare_phases(phase1_, phase2_)
        for key in output1:
            output1[key] += output1_[key]
        for key in output2:
            output2[key] += output2_[key]
    return output1, output2

