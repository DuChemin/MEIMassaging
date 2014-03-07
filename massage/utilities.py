
from pymei import MeiElement, MeiAttribute
import re

def has_C_clef(staffGrp):
	for staffDef in staffGrp.getChildren():
		if staffDef.getAttribute('clef.shape').getValue() == 'C':
			return True
	return False

def get_all_staves(MEI_tree):
	return MEI_tree.getDescendantsByName('staff')

def get_descendants(MEI_tree, expr):	

	def parse_tokens(tokens):	
		
		def parse_token(token):
			
			def parse_attrs(token):
				
				def parse_attrs_str(attrs_str):
					res = []
					attr_pairs = attrs_str.split(",")
					for attr_pair in attr_pairs:
						if attr_pair == '':
							continue
						name_val = attr_pair.split("=")
						if len(name_val)>1:
							attr = MeiAttribute(name_val[0], name_val[1])
							res.append(attr)
						else:
							if WARNING:
								print "Warning: get_descendants(): invalid attribute specifier in expression: " + expr
					return res
				m = re.search("\[(.*)\]", token)
				attrs_str = ""
				if m != None:
					attrs_str = m.group(1)
				return parse_attrs_str(attrs_str)

			m = re.search("^([^\[]+)", token)
			elem = MeiElement(m.group(1))
			attrs = parse_attrs(token)
			for attr in attrs:
				elem.addAttribute(attr)
			return elem
			
		elems = []
		for t in tokens:
			elems.append(parse_token(t))
		return elems
	
	def match_elems(elems2match, el):
		tagname = el.getName()
		for e2m in elems2match:
			if e2m.getName() == tagname:
				match = True
				for atr in e2m.getAttributes():
					if atr.getName() == "n" and atr.getValue() == "1":
						if el.hasAttribute("n") and el.getAttribute("n").getValue() != "1":
							match = False
					elif not el.hasAttribute(atr.getName()) or el.getAttribute(atr.getName()).getValue() != atr.getValue():
						match = False
				if match:
					return True
		return False
		
	res = []
	descendants = MEI_tree.getDescendants()
	tokens = expr.split(" ")
	elems2match = parse_tokens(tokens)
	for el in descendants:
		if (match_elems(elems2match, el)):
			res.append(el)
	return res
	
	
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


class Meter:
	count = None
	unit = None
	def read(self, sDef):
		if sDef.hasAttribute('meter.count'):
			self.count = sDef.getAttribute('meter.count').getValue()
		if sDef.hasAttribute('meter.unit'):
			self.unit = sDef.getAttribute('meter.unit').getValue()
	def semibreves(self):
		return float(self.count) / float(self.unit)


def effective_meter(elem):
	"""Gets the effective time signature at a given location under a 
	<staff> element that is a descendent of the <music> element.
	"""
	staff_n = '1'
	staff = elem.lookBack('staff')
	if staff.hasAttribute('n'):
		staff_n = staff.getAttribute('n').getValue()
	last_scoreDef = elem.lookBack('scoreDef')
	all_scoreDefs = elem.lookBack('music').getDescendantsByName('scoreDef')
	meter = Meter()
	for scD in all_scoreDefs:
		meter.read(scD)
		stD = get_descendants(scD, 'staffDef[n=' + staff_n + ']')[0]
		meter.read(stD)
		if scD == last_scoreDef:
			break
	return meter
	
	
	