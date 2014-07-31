from constants import *
# from pymei import MeiElement

def double_cut_time(MEI_tree):
    """Changes all 2/2 time signatures to 4/2, as might be desired
    in the mensural repertory. A cut time symbol, if present,
    will be left intact.
    """
    all_scoredef = MEI_tree.getDescendantsByName('scoreDef')
    for scoredef in all_scoredef:
        meter_count = scoredef.getAttribute('meter.count').getValue()
        meter_unit = scoredef.getAttribute('meter.unit').getValue()
        if meter_count == '2' and meter_unit == '2':
            meter_count.addAttribute('meter.count', '4')
