from constants import *
from pymei import MeiElement
from utilities import get_all_staves


def get_original_staves(MEI_tree, alternates_list, original_staves_NUM):
    """Returns a list of all staff objects of which other staff objects
    are marked as supplied staves; i.e. the ones whose staff information
    should be removed, though their place in the staff group will be held.
    """
    # Now get list of actuall staff objects
    all_staves = get_all_staves(MEI_tree)
    original_staves = []
    for staff in all_staves:
        if staff.getAttribute('n').getValue() in original_staves_NUM:
            original_staves.append(staff)
    return original_staves


def get_original_staves_NUM(MEI_tree, alternates_list, var_type_list):
    """Get numbers of all original staves."""
    original_staves_NUM = []
    for i in alternates_list:
        if i[2] not in original_staves_NUM and i[1] in var_type_list:
            original_staves_NUM.append(i[2])
    return original_staves_NUM


def get_supplied_staves_NUM(MEI_tree, alternates_list, var_type_list):
    """Get numbers of all supplied staves."""
    supplied_staves_NUM = []
    for i in alternates_list:
        if i[0] not in supplied_staves_NUM and i[1] in var_type_list:
            supplied_staves_NUM.append(i[0])
    return supplied_staves_NUM


def get_supplied_staves(MEI_tree, alternates_list, var_type_list):
    """Returns a list of all staff objects that are substituting for
    other staves, and should be moved inside the <app> of those staves.
    """
    supplied_staves_NUM = get_supplied_staves_NUM(MEI_tree,
                                                  alternates_list,
                                                  var_type_list)
    # Now get list of actual staff objects
    all_staves = get_all_staves(MEI_tree)
    supplied_staves = []
    for staff in all_staves:
        if staff.getAttribute('n').getValue() in supplied_staves_NUM:
            supplied_staves.append(staff)
    return supplied_staves


def make_orig_app(MEI_tree, original_staves):
    """Based on the list of original staves, replace them
    with empty <app> elements. and remove the placeholder
    staff elements.
    """
    all_staves = get_all_staves(MEI_tree)
    # Go through all staves to maintain original order
    for staff in all_staves:
        parent_measure = staff.getParent()
        old_staff_n = staff.getAttribute('n').getValue()
        # For original staves, which should be replaced with <app>:
        if staff in original_staves:
            new_app = MeiElement('app')
            new_app.addAttribute('n', old_staff_n)
            # Add <app> where <staff> was, and delete the latter
            parent_measure.removeChild(staff)
            parent_measure.addChild(new_app)
        # Otherwise, remove it and add it again, so that it will
        # be in its proper (numerical-order) place.
        else:
            parent_measure.removeChild(staff)
            parent_measure.addChild(staff)


def move_supplied_staves(supplied_staves, al):
    """Move supplied staves to their proper place within the <app>
    element created in place of the original (placeholder) staff.
    """

    def orig(staff_n, alternates_list):
        """Return the number of staff that the given staff
        is substituting for.
        """
        for i in alternates_list:
            if i[0] == staff_n:
                return i[2]

    def staff_type(staff_n, alternates_list):
        """Return the type of alternate a given staff belongs to."""
        for i in alternates_list:
            if i[0] == staff_n:
                return i[1]

    def resp(staff_n, alternates_list):
        for i in alternates_list:
            if i[0] == staff_n:
                return i[3]

    for staff in supplied_staves:
        staff_n = staff.getAttribute('n').getValue()
        parent_measure = staff.getParent()
        sibling_apps = parent_measure.getChildrenByName('app')
        for app in sibling_apps:
            # If it's the right <app> element -- that is,
            # the number matches with the original staff
            # for this supplied staff
            if orig(staff_n, al) == app.getAttribute('n').getValue():
                new_rdg = MeiElement('rdg')
                # Number <rdg> with old staff number
                new_rdg.addAttribute('n', staff_n)
                # Add responsibility to new reading element
                if staff_type(staff_n, al) == RECONSTRUCTION:
                    new_rdg.addAttribute('resp', '#' + resp(staff_n, al))
                elif staff_type(staff_n, al) == CONCORDANCE:
                    new_rdg.addAttribute('source', '#' + resp(staff_n, al))
                new_rdg.addAttribute('type', staff_type(staff_n, al))
                app.addChild(new_rdg)
                new_rdg.addChild(staff)
                parent_measure.removeChild(staff)


def adjust_staff_group(MEI_tree, original_staves_NUM):
    """Adjusts <staffGrp> definitions by removing attributes
    """
    def removeAttributes_Except(staffDef, attlist):
        attrs = staffDef.getAttributes()
        for attr in attrs[:]:
            attr_name = attr.getName()
            if attr_name not in attlist:
                staffDef.removeAttribute(attr_name)

    all_staff_def = MEI_tree.getDescendantsByName('staffDef')
    for staff_def in all_staff_def:
        if staff_def.getAttribute('n').getValue() in original_staves_NUM:
            removeAttributes_Except(staff_def, ['n', 'label', 'xml:id'])


def supplied_staves(MEI_tree, alternates_list, var_type_list):
    original_staves_NUM = get_original_staves_NUM(MEI_tree,
                                                  alternates_list,
                                                  var_type_list,
                                                  )
    original_staves = get_original_staves(MEI_tree,
                                          alternates_list,
                                          original_staves_NUM,
                                          )
    supplied_staves = get_supplied_staves(MEI_tree, alternates_list, var_type_list)

    make_orig_app(MEI_tree, original_staves)
    move_supplied_staves(supplied_staves, alternates_list)
