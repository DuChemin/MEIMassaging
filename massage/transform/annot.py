def remove_annot_brackets(MEI_tree):
    """Removes all <annot> elements with type="bracket"."""

    all_annot = MEI_tree.getDescendantsByName('annot')
    for annot in all_annot:
        if annot.getAttribute('type').getValue() == 'bracket':
            annot.getParent().removeChild(annot)
