from pymei import MeiElement


def make_invisible_space(MEI_tree, handle_mRest=False):
    """Turns all invisible notes, rests and mRests into
    <space> elements.
    """

    all_note_rest = MEI_tree.getDescendantsByName('note rest')
    all_mRest = MEI_tree.getDescendantsByName('mRest')

    # Replace notes and rests with spaces
    for item in all_note_rest:
        try:
            if item.getAttribute('visible').getValue() == 'false':
                space = MeiElement('space')
                attributes = item.getAttributes()
                for attr in attributes:
                    # Don't add octave or pitch attributes to space
                    if attr.getName() not in ['oct', 'pname']:
                        space.addAttribute(attr)
                # If mRest, calculate duration here?
                parent = item.getParent()
                parent.addChildBefore(item, space)
                parent.removeChild(item)
        except:  # doesn't have attribute `visible`
            pass
    # Replace mRests with nothing -- just remove them
    # Not currently supported by MEItoVexFlow
    if handle_mRest:
        for item in all_mRest:
            try:
                if item.getAttribute('visible').getValue() == 'false':
                    item.getParent().removeChild(item)
            except:  # doesn't have attribute `visible`
                pass
