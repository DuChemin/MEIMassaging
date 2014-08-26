from constants import *
from pymei import MeiElement
from utilities import chain_elems


def sources_and_editors(MEI_tree, alternates_data):
    """add the sourceDesc element, the source elements, and
    the editor elements to the mei header
    """
    def add_source(sourceDesc, adi):
        existing = sourceDesc.getDocument().getElementById(adi[3])
        if not existing:
            source = MeiElement('source')
            source.id = adi[3]
            source.addAttribute('type', adi[1])
            sourceDesc.addChild(source)

    def add_editor(titleStmt, ali):
        existing = titleStmt.getDocument().getElementById(adi[3])
        if not existing:
            editor = MeiElement('editor')
            editor.id = ali[3]
            # Using 'replace' simply to have more natural name for a person
            editor.addAttribute('type', adi[1].replace('ction', 'ctor'))
            titleStmt.addChild(editor)

    for adi in alternates_data:
        if adi[1] == RECONSTRUCTION:
            add_editor(chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'titleStmt']), adi)
        elif adi[1] == EMENDATION:
            add_editor(chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'titleStmt']), adi)
        elif adi[1] == CONCORDANCE:
            add_source(chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'sourceDesc']), adi)
        elif adi[0] != adi[2] and adi[1] == VARIANT:
            add_source(chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'sourceDesc']), adi)
        else:
            pass
