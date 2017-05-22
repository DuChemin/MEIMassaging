from constants import *
from alt import get_color, color_matches
from pymei import MeiElement
from utilities import staff_role


def mark_ficta(MEI_tree, color_we_want, alternates_list, remove_color=True):
    """If a staff is not an emendation, reconstruction, etc.,
    change colored notes with accidentals into ficta.
    """
    all_measures = MEI_tree.getDescendantsByName('measure')
    for measure in all_measures:
        for staff in measure.getDescendantsByName('staff'):
            staff_n = staff.getAttribute('n').getValue()
            # Don't make accidentals in a reconstructed staff ficta.
            # Note that if there are accidentals in a VARIANT or
            # CONCORDANCE staff, it will be necessary to use
            # different colors!
            if staff_role(staff_n, alternates_list) != RECONSTRUCTION:
                notes_in_staff = staff.getDescendantsByName('note')
                for note in notes_in_staff:
                    if color_matches(get_color(note), color_we_want):
                        mark_accid_as_editorial(note)
                        if remove_color:
                            note.removeAttribute('color')

def mark_accid_as_editorial(note):
    """If the note given has an accidental, mark that accidental
    as editorial and display it above the note.
    """
    # There should be zero or one accid elements in the list,
    # but it's easier and maybe safer to get a list of "all"
    # the accidental elements contained within the note.
    note_accidentals = note.getDescendantsByName('accid')
    for accid in note_accidentals:
        supplied_element = MeiElement('supplied')
        supplied_element.addAttribute('reason', 'edit')
        note.addChild(supplied_element)

        accid.addAttribute('func', 'edit')
        accid.addAttribute('place', 'above')
        # The accidental SHOULD be the child of <note>, but
        # just in case we'll get its parent.
        accid_parent = accid.getParent()
        accid_parent.removeChild(accid)
        # Then add the <accid> element to <supplied>
        supplied_element.addChild(accid)
        
