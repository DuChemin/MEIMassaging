
from pymei import MeiElement
import re

def has_C_clef(staffGrp):
	for staffDef in staffGrp.getChildren():
		if staffDef.getAttribute('clef.shape').getValue() == 'C':
			return True
	return False

def get_all_staves(MEI_tree):
	return MEI_tree.getDescendantsByName('staff')

def get_descendants_with_attribute_value(MEI_tree, names, attr, value):
	res = []
	descendants = MEI_tree.getDescendantsByName(names)
	for elem in descendants:
		if elem.hasAttribute(attr) and elem.getAttribute(attr).getValue() == value:
			res.append(elem)
	return res

def get_children_with_attribute_value(MEI_tree, names, attr, value):
	res = []
	children = MEI_tree.getChildrenByName(names)
	for elem in children:
		if elem.hasAttribute(attr) and elem.getAttribute(attr).getValue() == value:
			res.append(elem)
	return res
	
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

def source_name2NCName(source_name, prefix="RISM"):
	# replace illegal characters:
	#   * '/' --> '-'
	# add prefix if the string starts with a digit
	res = re.sub("\s+", "_", source_name)
	res = re.sub("/", "-", res)
	res = re.sub("[^a-zA-Z0-9_\-.]", "_", res)
	res = re.sub("^([0-9\-.])", prefix+"\g<1>", res)
	return res
