
from constants import *
from pymei import MeiElement
from utilities import chain_elems

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
	
	def mergeClefAttributes(staffDef, clef):
		# merge the following attributes:
		#  * shape 
		#  * line 
		#  * oct
		#  * dis
		#  * dis.place
		def mergeAttr(attr_name):
			print 'merging attributes ' + attr_name
			if (clef.hasAttribute(attr_name)):
				print 'merging attributes ' + attr_name + ' new value: ' +  clef.getAttribute(attr_name).getValue()
				staffDef.addAttribute('clef.' + attr_name, clef.getAttribute(attr_name).getValue())
		mergeAttr('shape')
		mergeAttr('line')
		mergeAttr('oct')
		mergeAttr('dis')
		mergeAttr('dis.place')

	def mergeScoreDefAttributes(scoreDef1, scoreDef2):
		# merge the following attributes:
		#  * meter.count 
		#  * meter.unit 
		#  * meter.sym
		#  * clef.line
		#  * clef.shape
		#  * clef.oct
		#  * clef.dis
		#  * clef.dis.place
		#  * key.sig
		#  * key.pname
		#  * key.accid
		#  * key.mode
		#  * key.sig.mixed

		def mergeAttr(attr_name):
			if (scoreDef2.hasAttribute(attr_name)):
				scoreDef1.addAttribute(attr_name, scoreDef2.getAttribute(attr_name).getValue())
		mergeAttr('meter.count')
		mergeAttr('meter.unit')
		mergeAttr('meter.sym')
		mergeAttr('clef.line')
		mergeAttr('clef.oct')
		mergeAttr('clef.dis')
		mergeAttr('clef.dis.place')
		mergeAttr('key.sig')
		mergeAttr('key.pname')
		mergeAttr('key.accid')
		mergeAttr('key.mode')
		mergeAttr('key.sig.mixed')
				
	# copy initial scoreDef to meiHead/workDesc/work/incip/score/
	scoreDefs = MEI_tree.getDescendantsByName('scoreDef')
	# make a copy of the main scoreDef
	mainScoreDef = MeiElement(scoreDefs[0])	
	# remove unwanted staves:
	#  - Reconstructed (placeholder) staves
	#  - Reconstruction (actual reconstruction) staves
	#  - Emendation staves
	staffDefs = mainScoreDef.getDescendantsByName('staffDef')
	for staffDef in staffDefs:
		staff_n = staffDef.getAttribute('n').getValue() 
		if (is_placeholder(staff_n, alternates_list) or 
				staff_role(staff_n, alternates_list) == RECONSTRUCTION or
				staff_role(staff_n, alternates_list) == EMENDATION):
			staffDef.parent.removeChild(staffDef)
	meiHead = MEI_tree.getDescendantsByName('meiHead')[0]
	
	workDesc = MeiElement('workDesc')
	head_score = chain_elems(meiHead, ['workDesc', 'work', 'incip', 'score'])
	head_score.addChild(mainScoreDef)
	# TODO: remove the milestone scoreDef and update the
	# main scoreDef accordingly.
	# In addition: 
	#  1. find <clef> elements (they should be in the first measure: 
	#     assert this, and signal warning if it's not the case)
	#  2. update main scoreDef according to <clef>

	music = MEI_tree.getDescendantsByName('music')[0]
	section = music.getDescendantsByName('section')[0]
	
	#TODO: NEXT!!!!
	# msScoreDefs = music.getDescendantsByName('scoreDef')
	
	# assert whether this scoreDef appears right after the incipit measure;
	# if not, issue warning.
	
	clefs = section.getDescendantsByName('clef')
	for clef in clefs:
		clef_valid = False
		clef_in_measure = False
		clef_in_staff = False
		if (clef.hasAncestor('measure')): 
			measure = clef.getAncestor('measure')
			if (measure.hasAttribute('n') and measure.getAttribute('n').getValue() == '1'):
				clef_in_measure = True
		if (clef.hasAncestor('staff')):
			staff = clef.getAncestor('staff')
			clef_in_staff = True
		
		if (not clef_in_measure): 
			print "WARNING: <clef> is only valid under the first <measure>."
			continue

		if (not clef_in_staff): 
			print "WARNING: <clef> is only valid under a <staff>."
			continue

		if (staff.hasAttribute('n')):
			clef_staff_n = staff.getAttribute('n').getValue()
		else:
			clef_staff_n = '1'

		staffDefs = music.getDescendantsByName('staffDef')
		for staffDef in staffDefs:
			staff_n = staffDef.getAttribute('n').getValue()
			if (staff_n == clef_staff_n):
				mergeClefAttributes(staffDef, clef)
		
			
	
