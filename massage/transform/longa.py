
from constants import *
# from pymei import MeiElement

def longa(MEI_tree):
    """Changes duration of final note in each part to a longa."""
    all_measures = MEI_tree.getDescendantsByName('measure')
    last_measure = all_measures[-1]
    last_staves = last_measure.getChildren()
    for staff in last_staves:
        all_last_notes = staff.getDescendantsByName('note')
        try:
            last_note_of_staff = all_last_notes[-1]
            # The following line *replaces* the existing @dur.
            last_note_of_staff.addAttribute('dur', LONGA)
            last_note_of_staff.addAttribute('dur.ges', '4096p')
        except IndexError:
            pass
