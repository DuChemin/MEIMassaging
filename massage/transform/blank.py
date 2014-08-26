from pymei import MeiElement
from constants import *


def blank_out(el):
    """Replace all <rest> and <mRest> elements that are descendants
    of `el` with <space> elements.
    """
    all_rests = (el.getDescendantsByName('rest') +
                 el.getDescendantsByName('mRest'))
    for rest in all_rests:
        space = MeiElement('space')
        rest_attributes = rest.getAttributes()
        for attr in rest_attributes:
            space.addAttribute(attr)
        parent = rest.getParent()
        parent.removeChild(rest)
        parent.addChild(space)


def empty_staves(MEI_tree):
    """Replaces all <rest> and <mRest> elements with <space>
    that have <rdg type="blank"> as an ancestor.
    """

    all_rdg = MEI_tree.getDescendantsByName('rdg')
    for rdg in all_rdg:
        try:
            if rdg.getAttribute('type').getValue() == BLANK:
                blank_out(rdg)
        except:
            pass
