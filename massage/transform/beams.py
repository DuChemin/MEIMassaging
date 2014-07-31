def eliminate_bad_beams(MEI_tree):
    """Removes all beams that contain a single note."""

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
    # list. We will go through this list one by one and construct
    # a new list of children. After adding each element to the
    # list, we remove it from its parent.
    all_layers = MEI_tree.getDescendantsByName('layer')
    for layer in all_layers:
        old_layer_items = layer.getChildren()
        new_layer_items = []
        for item in old_layer_items:
            # If the item in the list is a singleton beam, then
            # we should not add the beam to the revised list of elements
            # to add; instead, we should add the beam's children,
            # of which there is probably only one.
            if is_singleton_beam(item):
                beam_children = item.getChildren()
                for child in beam_children:
                    new_layer_items.append(child)
                    child.getParent().removeChild(child)
            # If the item in the list is anything other than a
            # singleton beam, we simply add it to our revised list.
            else:
                new_layer_items.append(item)
                item.getParent().removeChild(item)
        # Now that we have the complete revised list, we remove all
        # children from the layer and add the children from the revised
        # list one by one.
        for item in new_layer_items:
            layer.addChild(item)
