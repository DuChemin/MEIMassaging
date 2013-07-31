
from constants import *
from pymei import MeiElement

def arranger(MEI_tree):
	"""Changes all occurrence of the <arranger> tag to <editor>."""
	all_arranger = MEI_tree.getDescendantsByName('arranger')
	for arranger in all_arranger:
		parent = arranger.getParent()
		editor = MeiElement('editor')
		arranger_children = arranger.getChildren()
		arranger_value = arranger.getValue()
		for child in arranger_children:
			editor.addChild(child)
		editor.setValue(arranger_value)
		parent.addChild(editor)
		parent.removeChild(arranger)
