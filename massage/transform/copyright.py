def use_restrict(MEI_tree, copyright_text):
    """Adds the string in `copyright_text` to the <useRestrict>
    element in the MEI header, if such an element is present.

    Could be enhanced in the future by being able to create
    such an element.
    """
    all_useRestrict = MEI_tree.getDescendantsByName('useRestrict')
    for el in all_useRestrict:
        el.setText(copyright_text)
