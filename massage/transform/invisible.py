from pymei import MeiElement


def make_invisible_space(MEI_tree):
    """Turns all invisible notes, rests and mRests into
    <space> elements.
    """

    all_items = (MEI_tree.getDescendantsByName('note') +
                 MEI_tree.getDescendantsByName('rest') +
                 MEI_tree.getDescendantsByName('mRest')
                 )
    for item in all_items:
        try:
            if item.getAttribute('visible').getValue() == 'false':
                space = MeiElement('space')
                attributes = item.getAttributes()
                for attr in attributes:
                    space.addAttribute(attr)
                parent = item.getParent()
                parent.removeChild(item)
                parent.addChild(space)
        except:
            pass
