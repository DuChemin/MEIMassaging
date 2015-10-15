# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')

from constants import *
from pymei import documentFromFile


PITCH_CLASSES = {
    'c': u'C',
    'd': u'D',
    'e': u'E',
    'f': u'F',
    'g': u'G',
    'a': u'A',
    'b': u'B',
}

ACCIDENTALS = {
    'ff': u'𝄫',
    'f': u'♭',
    'nf': u'♭',
    'n': u'',
    'ns': u'♯',
    's': u'♯',
    'ss': u'𝄪',
}


def last_bass_tone(MEI_tree):
    """ Returns the final tone in the lowest staff.
    Returns None if there is nothing in the last measure of
    the lowest staff, or if there are no staves in the last
    measure. The tone is formatted as a unicode string.

    Another note of caution: it's possible that the bass is
    not the lowest-sounding voice at a particular instant.
    This function ignores this possibility, which is unlikely
    to occur at the last tone (and would then be notable!).
    If the bass is not present at all at the last tone, then
    the function will return None, which of course bears looking
    into regardless.
    """

    all_measures = MEI_tree.getDescendantsByName('measure')
    last_measure = all_measures[-1]
    # Gets all the staves in the last measure
    last_staves = last_measure.getChildrenByName('staff')
    try:
        bass_staff = last_staves[-1]
        last_bass_note = bass_staff.getChildrenByName('note')[-1]
        last_bass_pname = last_bass_note.getAttribute('pname').getValue()
        if last_bass_note.getAttribute('accid'):
            last_bass_accid = last_bass_note.getAttribute('accid').getValue()
        else:
            last_bass_accid = 'n'  # for natural
        return PITCH_CLASSES[last_bass_pname] + ACCIDENTALS[last_bass_accid]

    except IndexError:
        # Error because no final bass tone?
        return None

if __name__ == "__main__":
    MEI_filename = raw_input('Enter a file name: ')
    res = documentFromFile(MEI_filename)
    MEI_doc = res.getMeiDocument()
    MEI_tree = MEI_doc.getRootElement()
    print last_bass_tone(MEI_tree)
