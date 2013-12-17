
from constants import *
from pymei import MeiElement
from utilities import chain_elems, get_children_with_attribute_value

def sources_and_editors(MEI_tree, alternates_data):
	"""add the sourceDesc element, the source elements, and 
	the editor elements to the mei header
	"""	
	def add_source(sourceDesc, adi):
		existing = sourceDesc.getDocument().getElementById(adi[3])
		if not existing:
			source = MeiElement('source')
			source.id = adi[3]
			sourceDesc.addChild(source)

	def add_editor(titleStmt, ali):
		existing = titleStmt.getDocument().getElementById(adi[3])
		if not existing:
			editor = MeiElement('editor')
			editor.id = ali[3]
			titleStmt.addChild(editor)

	titleStmt = chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'titleStmt'])
	sourceDesc = chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'sourceDesc'])
	for adi in alternates_data:
		if adi[1] == RECONSTRUCTION or adi[1] == EMENDATION:
			add_editor(titleStmt, adi)
		if adi[0] != adi[2] and adi[1] == VARIANT:
			add_source(sourceDesc, adi)

# END OF FILE

