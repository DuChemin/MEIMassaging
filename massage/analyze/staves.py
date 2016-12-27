import sys
import logging
sys.path.insert(0, '..')

from constants import *
from re import split
from utilities import source_name2NCName
from utilities import staff_role


def is_empty(MEI_tree, staff_n):
    """Returns True if there are no notes associated with staves
    with n=staff_num; False otherwise.
    """
    all_staff = MEI_tree.getDescendantsByName('staff')
    for staff in all_staff:
        try:
            if staff.getAttribute('n').getValue() == str(staff_n):
                all_notes = staff.getDescendantsByName('note')
                if len(all_notes) > 0:
                    return False
        except:
            pass
    return True


def staff_list(MEI_tree):
    def get_role_from_name(staff_name):
        if 'recon' in staff_name.lower():
            return RECONSTRUCTION
        elif 'emend' in staff_name.lower() or 'amend' in staff_name.lower():
            return EMENDATION
        elif 'concord' in staff_name.lower():
            return CONCORDANCE
        elif 'ignore' in staff_name.lower():
            return IGNORED
        # Make VARIANT the default case
        else:
            return VARIANT

    all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
    staff_list = []
    if len(all_staffGrp) < 1:
        logging.error("Error: No staffGrp in file.")
    else:
        if len(all_staffGrp) > 1:
            logging.warning("Warning: more than one <staffGrp>; using first occurrence.")
        staffGrp = all_staffGrp[0]
        for staffDef in staffGrp.getDescendantsByName('staffDef'):
            staff_name = staffDef.getAttribute('label').getValue()
            staff_name_split = split('_', staff_name)
            staff_n = staffDef.getAttribute('n').getValue()

            staff_voice = staff_name_split[0]
            # VARIANT is the default -- original staves are
            # marked as variants of themselves.
            staff_type = VARIANT
            staff_source = ''
            # If it's a special staff (true variant, reconstruction, etc.)
            if len(staff_name_split) > 1:
                staff_type = get_role_from_name(staff_name)
                if len(staff_name_split) > 2:
                    staff_source = staff_name_split[2]
            # If it's an empty staff
            if is_empty(MEI_tree, staff_n):
                staff_type = BLANK
                staff_source = staff_name

            staff_list.append(
                (staff_name,
                 staff_voice,
                 staff_type,
                 source_name2NCName(staff_source),
                 staff_n,
                 )
            )
    return staff_list


def alternates_list(staff_list):

    def n_of_voice(staff_voice, staff_list):
        for sli in staff_list:
            if sli[0] == staff_voice:
                return sli[4]

    result = []
    for staff_list_item in staff_list:
        staff_name = staff_list_item[0]
        staff_voice = staff_list_item[1]
        staff_type = staff_list_item[2]
        staff_source = staff_list_item[3]
        staff_n = staff_list_item[4]
        if staff_voice == staff_name:
            res_item = (staff_n, staff_type, staff_n, staff_source)
        else:
            staff_voice_n = n_of_voice(staff_voice, staff_list)
            if (staff_voice_n):
                res_item = (staff_n, staff_type, staff_voice_n, staff_source)
            else:
                logging.error("Cannot find corresponding staff for staff: " +
                              str(staff_list_item))
        result.append(res_item)
    return result
