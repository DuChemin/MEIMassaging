def cleanup_all_attributes(MEI_tree):
    remove_incipit_meter(MEI_tree)
    remove_page_dimensions(MEI_tree)
    remove_ppq(MEI_tree)
    remove_key_mode(MEI_tree)
    remove_color(MEI_tree)


def remove_incipit_meter(MEI_tree):
    """Remove meter.count and meter.unit from <scoreDef>
    elements inside an incipit.
    """
    all_incip = MEI_tree.getDescendantsByName('incip')
    for incip in all_incip:
        scoreDefs = incip.getDescendantsByName('scoreDef')
        for element in scoreDefs:
            if element.hasAttribute('meter.count'):
                element.removeAttribute('meter.count')
            if element.hasAttribute('meter.unit'):
                element.removeAttribute('meter.unit')


def remove_page_dimensions(MEI_tree):
    """Remove page dimension attributes from <scoreDef> elements."""
    page_dimension_attributes = [
        'page.botmar',
        'page.topmar',
        'page.leftmar',
        'page.rightmar',
        'page.height',
        'page.width',
    ]
    all_scoreDef = MEI_tree.getDescendantsByName('scoreDef')
    for element in all_scoreDef:
        for attr_name in page_dimension_attributes:
            if element.hasAttribute(attr_name):
                element.removeAttribute(attr_name)


def remove_ppq(MEI_tree):
    """Remove ppq attributes from <scoreDef> elements."""
    all_scoreDef = MEI_tree.getDescendantsByName('scoreDef')
    for element in all_scoreDef:
        if element.hasAttribute('ppq'):
            element.removeAttribute('ppq')


def remove_key_mode(MEI_tree):
    """Remove key.mode from <staffDef> elements."""
    all_staffDef = MEI_tree.getDescendantsByName('staffDef')
    for element in all_staffDef:
        if element.hasAttribute('key.mode'):
            element.removeAttribute('key.mode')


def remove_color(MEI_tree):
    """Remove the color attribute from all notes and rests."""
    all_notes_rests = MEI_tree.getDescendantsByName('note rest mRest')
    for element in all_notes_rests:
        if element.hasAttribute('color'):
            element.removeAttribute('color')
