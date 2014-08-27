from pymei import MeiElement


def make_invisible_space(MEI_tree):
    """Turns all invisible notes, rests and mRests into
    <space> elements.
    """

    notes = MEI_tree.getDescendantsByName('note')
    rests = MEI_tree.getDescendantsByName('rest')
    mRests = MEI_tree.getDescendantsByName('mRest')

    for list_of_elements in [notes, rests, mRests]:
        for item in list_of_elements:
            try:
                if item.getAttribute('visible').getValue() == 'false':
                    space = MeiElement('space')
                    attributes = item.getAttributes()
                    for attr in attributes:
                        space.addAttribute(attr)
                    # If mRest, need to calculate duration here...
                    parent = item.getParent()
                    parent.removeChild(item)
                    parent.addChild(space)
            except:
                pass
