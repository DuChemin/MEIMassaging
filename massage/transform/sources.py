
from constants import *
from pymei import MeiElement
from utilities import chain_elems, get_children_with_attribute_value

def sources_and_editors(MEI_tree, alternates_data):
	"""add the sourceDesc element, the source elements, and 
	the editor elements to the mei header
	"""	
	def add_source(sourceDesc, adi):
		existing = get_children_with_attribute_value(sourceDesc, 'source', 'xml:id', adi[3])
		if len(existing) == 0:
			source = MeiElement('source')
			source.addAttribute('xml:id', adi[3])
			sourceDesc.addChild(source)

	def add_editor(titleStmt, ali):
		existing = get_children_with_attribute_value(titleStmt, 'editor', 'xml:id', adi[3])
		if len(existing) == 0:
			editor = MeiElement('editor')
			editor.addAttribute('xml:id', ali[3])
			titleStmt.addChild(editor)

	titleStmt = chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'titleStmt'])
	sourceDesc = chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'sourceDesc'])
	for adi in alternates_data:
		if adi[1] == RECONSTRUCTION or adi[1] == EMENDATION:
			add_editor(titleStmt, adi)
		if adi[0] != adi[2] and adi[1] == VARIANT:
			add_source(sourceDesc, adi)

# END OF FILE

