
from pymei import MeiElement

def has_C_clef(staffGrp):
	for staffDef in staffGrp.getChildren():
		if staffDef.getAttribute('clef.shape').getValue() == 'C':
			return True
	return False

def get_all_staves(MEI_tree):
	return MEI_tree.getDescendantsByName('staff')

def chain_elems(start_elem, elems):
	def getOrAddChild(mei_elem, child_name):
		children = mei_elem.getChildrenByName(child_name)
		if len(children) > 0:
			return children
		mei_elem.addChild(MeiElement(child_name))
		return mei_elem.getChildrenByName(child_name)

	if elems == []:
		return start_elem
	children = getOrAddChild(start_elem, elems[0])
	return chain_elems(children[0], elems[1:])