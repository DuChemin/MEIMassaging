import sys
sys.path.insert(0, '..')

# from constants import *


def has_editor_element(MEI_tree):
    all_editor_elements = MEI_tree.getDescendantsByName('editor')
    return all_editor_elements != []


def has_arranger_element(MEI_tree):
    all_arranger_elements = MEI_tree.getDescendantsByName('arranger')
    return all_arranger_elements != []


def editor_name(MEI_tree):
    """Returns <editor> value, if it exists, or if not, then
    at least <arranger>. Return an empty string if neither exists.
    """
    if has_editor_element(MEI_tree):
        TAG = 'editor'
    else:
        TAG = 'arranger'
    all_editor_elements = MEI_tree.getDescendantsByName(TAG)
    if len(all_editor_elements) > 0:
        return all_editor_elements[0].getValue()
    else:
        return ''
