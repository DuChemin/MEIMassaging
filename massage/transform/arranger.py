
from constants import *
from pymei import MeiElement

def arranger(MEI_tree, arranger_editor):
	if arranger_editor:
		all_arranger = MEI_tree.getDescendantsByName('arranger')
		for arranger in all_arranger:
			parent = arranger.getParent()
			editor = MeiElement('editor')
			arranger_children = arranger.getChildren()
			for child in arranger_children:
				editor.addChild(child)
			parent.addChild(editor)
			parent.removeChild(arranger)
