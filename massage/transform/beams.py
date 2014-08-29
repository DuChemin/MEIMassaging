from pymei import MeiElement

def eliminate_bad_beams(MEI_tree):
    """Removes all beams that contain a single note.
    Warning: should not be used for staves containing
    more than one layer.
    """

    def is_singleton_beam(element):
        """Function returns True iff an MEI element is
        a beam AND the element has no more than one note/rest.
        """
        if element.getName() == 'beam':
            notes_inside = element.getDescendantsByName('note')
            rests_inside = element.getDescendantsByName('rest')
            return len(notes_inside) + len(rests_inside) < 2
        else:
            return False

    # Get all layers in the MEI file, and get its children as a
    # list. We will go through this list and if we find a singleton
    # beam, we will add its children to the layer at the location
    # of the beam. Then we will remove the beam.
    all_layers = MEI_tree.getDescendantsByName('layer')
    for layer in all_layers:
        for item in layer.getChildren():
            if is_singleton_beam(item):
                # Add the children to the layer
                beam_children = item.getChildren()
                for child in beam_children:
                    item.removeChild(child)
                    layer.addChildBefore(item, child)
                # Remove the beam from the layer
                layer.removeChild(item)
