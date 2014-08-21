from constants import *
from pymei import MeiElement


def change_arranger_element(MEI_tree):
    """Changes all occurrence of the <arranger> tag to <editor>"""
    all_arranger = MEI_tree.getDescendantsByName('arranger')
    for arranger in all_arranger:
        parent = arranger.getParent()
        editor = MeiElement('editor')
        arranger_children = arranger.getChildren()
        arranger_value = arranger.getValue()
        for child in arranger_children:
            editor.addChild(child)
        editor.setValue(arranger_value)
        parent.addChild(editor)
        parent.removeChild(arranger)


def change_arranger_role(MEI_tree):
    """Changes all occurrences of 'arranger' as a @role
    in the element <persName> to 'editor'.
    """
    all_persName = MEI_tree.getDescendantsByName('persName')
    for persName in all_persName:
        if (persName.hasAttribute('role') and
                persName.getAttribute('role').getValue() == 'arranger'):
            persName.addAttribute('role', 'editor')


def arranger(MEI_tree):
    """Reinterprets arranger as editor in all occurrences."""
    change_arranger_element(MEI_tree)
    change_arranger_role(MEI_tree)
