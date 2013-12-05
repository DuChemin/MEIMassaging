
from constants import *
from pymei import MeiElement

def obliterate_incipit(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	for measure in all_measures:
		if measure.getAttribute('n').getValue() == '1':
			measure.getParent().removeChild(measure)

def renumber_measures(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	for measure in all_measures:
		# Get measure number attribute
		attr_measure_number = measure.getAttribute('n')
		val_measure_number = attr_measure_number.getValue()
		# Reduce number by one
		attr_measure_number.setValue(str(eval(val_measure_number) - 1))

def orig_clefs(MEI_tree, alternates_list):
	def is_placeholder(staff_n, alternates_list):
		"""a staff is PLACEHOLDER if there's at least one other staff that is a RECONSTRUCTION of it."""
		for a in alternates_list:
			# if a is RECONSTRUCTION of alt_list_item:
			if a[2] == staff_n and a[1] == RECONSTRUCTION:
				return True
		return False
		
	def staff_role(staff_n, alternates_list):
		for a in alternates_list:
			if a[0] == staff_n:
				return a[1]

	def getOrAddChild(mei_elem, child_name):
		children = mei_elem.getChildrenByName(child_name)
		if len(children) > 0:
			return children
		mei_elem.addChild(MeiElement(child_name))
		return mei_elem.getChildrenByName(child_name)

	def chain_elems(start_elem, elems):
		if elems == []:
			return start_elem
		children = getOrAddChild(start_elem, elems[0])
		return chain_elems(children[0], elems[1:])
				
	# copy initial scoreDef to meiHead/workDesc/work/incip/score/
	scoreDefs = MEI_tree.getDescendantsByName('scoreDef')
	# make a copy of the main scoreDef
	incipScoreDef = MeiElement(scoreDefs[0])	
	# remove unwanted staves:
	#  - Reconstructed (placeholder) staves
	#  - Reconstruction (actual reconstruction) staves
	#  - Emendation staves
	staffDefs = incipScoreDef.getDescendantsByName('staffDef')
	for staffDef in staffDefs:
		staff_n = staffDef.getAttribute('n').getValue() 
		if (is_placeholder(staff_n, alternates_list) or 
				staff_role(staff_n, alternates_list) == RECONSTRUCTION or
				staff_role(staff_n, alternates_list) == EMENDATION):
			staffDef.parent.removeChild(staffDef)
	meiHead = MEI_tree.getDescendantsByName('meiHead')[0]
	
	workDesc = MeiElement('workDesc')
	score = chain_elems(meiHead, ['workDesc', 'work', 'incip', 'score'])
	score.addChild(incipScoreDef)
	# TODO: decide whether it is necessary to remove the milestone scoreDef and update the
	# main scoreDef accordingly.
