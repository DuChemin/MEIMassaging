def cleanup_all_elements(MEI_tree):
    remove_annot_brackets(MEI_tree)
    remove_metersig(MEI_tree)
    remove_empty_persname(MEI_tree)
    remove_empty_syllables(MEI_tree)
    remove_anchored_text(MEI_tree)


def remove_annot_brackets(MEI_tree):
    """Removes all <annot> elements with type="bracket"."""
    all_annot = MEI_tree.getDescendantsByName('annot')
    for annot in all_annot:
        if annot.getAttribute('type').getValue() == 'bracket':
            annot.getParent().removeChild(annot)


def remove_metersig(MEI_tree):
    """Removes all <meterSig> elements."""
    all_meterSig = MEI_tree.getDescendantsByName('meterSig')
    for element in all_meterSig:
        element.getParent().removeChild(element)


def remove_empty_persname(MEI_tree):
    """Removes all empty <persName> elements. If this leaves
    an empty parent, remove that parent as well.
    """
    all_persName = MEI_tree.getDescendantsByName('persName')
    for element in all_persName:
        parent = element.getParent()
        if len(element.getChildren()) == 0:
            parent.removeChild(element)
            # Remove parent if also empty
            if len(parent.getChildren()) == 0:
                parent.getParent().removeChild(parent)


def remove_empty_syllables(MEI_tree):
    """Removes all syllables with no text inside."""
    all_verses = MEI_tree.getDescendantsByName('verse')
    for verse in all_verses:
        syllables_in_verse = verse.getDescendantsByName('syl')
        for syl in syllables_in_verse:
            # Delete the syllable if it has no text inside
            if not syl.getValue():
                verse.removeChild(syl)


def remove_anchored_text(MEI_tree):
    """Removes all <anchoredText> elements from the MEI tree."""
    all_anchoredText = MEI_tree.getDescendantsByName('anchoredText')
    for element in all_anchoredText:
        element.getParent().removeChild(element)
