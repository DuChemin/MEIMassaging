
from constants import *
from pymei import MeiElement
from utilities import get_all_staves

def get_ignored_staves(alternates_list):
    all_ignored = []
    for i in alternates_list:
        if i[2] == IGNORED:
            all_ignored.append(i[0])
    return all_ignored

def remove_ignored_staves(MEI_tree, ignored_staves):
    for staff in get_all_staves(MEI_tree):
        if staff.getAttribute('n').getValue() in ignored_staves:
            staff.getParent().removeChild(staff)

def remove_ignored_staff_groups(MEI_tree, ignored_staves):
    all_staff_def = MEI_tree.getDescendantsByName('staffDef')
    for staff_def in all_staff_def:
        if staff_def.getAttribute('n').getValue() in ignored_staves:
            staff_def.getParent().removeChild(staff_def)

def ignored(MEI_tree, alternates_list):
    ignored_staves = get_ignored_staves(alternates_list)
    remove_ignored_staves(MEI_tree, ignored_staves)
    remove_ignored_staff_groups(MEI_tree, ignored_staves)
