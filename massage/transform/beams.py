from pymei import MeiElement

def eliminate_bad_beams(MEI_tree):
    """Removes all beams that contain a single note.
    Warning: should not be used for staves containing
    more than one layer.
    """

    def is_singleton_beam(element):
        """Function returns True iff an MEI element is
        a beam AND the element has no more than one note/rest
        """
        if element.getName() == 'beam':
            notes_inside = element.getDescendantsByName('note')
            rests_inside = element.getDescendantsByName('rest')
            return len(notes_inside) + len(rests_inside) < 2
        else:
            return False

    # Get all layers in the MEI file, and get its children as a
    # list. We will go through this list one by one and add them
    # to our new layer. Before adding each element to the new
    # layer, we remove it from the old one.
    all_layers = MEI_tree.getDescendantsByName('layer')
    for layer in all_layers:
        old_layer_items = layer.getChildren()
        new_layer = MeiElement('layer')
        for item in old_layer_items:
            # If the item in the list is a singleton beam, then
            # we should not add the beam to the new layer; instead,
            # we should add the beam's children, of which there is
            # probably only one.
            if is_singleton_beam(item):
                beam_children = item.getChildren()
                for child in beam_children:
                    child.getParent().removeChild(child)
                    new_layer.addChild(child)
            # If the item in the list is anything other than a
            # singleton beam, we simply add it to our new layer.
            else:
                item.getParent().removeChild(item)
                new_layer.addChild(item)
        # Now that we have the complete new layer, we remove the old
        # one from its parent and add the new one.
        staff = layer.getParent()
        staff.deleteAllChildren()
        staff.addChild(new_layer)
