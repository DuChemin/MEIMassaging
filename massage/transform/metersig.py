def remove_metersig(MEI_tree):
    """Removes all <meterSig> elements."""

    all_metersig = MEI_tree.getDescendantsByName('meterSig')
    for element in all_metersig:
        element.getParent().removeChild(element)
