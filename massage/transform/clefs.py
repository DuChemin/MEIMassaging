
from constants import *
from utilities import has_C_clef
from pymei import MeiElement

def reg_clefs_choice(staffGrp_orig):
	"""Returns <choice> tag with a <reg> and an <orig>.
	The <orig> tag contains the <staffGrp> of original
	clefs that was already there. The <reg> tag contains
	the <staffGrp> with regularized clefs, computed from
	the original clefs (e.g. tenor clef becomes treble_8).
	Compare orig_clefs_choice.
	"""
	# Create new MEI elements
	choice = MeiElement('choice')
	orig = MeiElement('orig')
	reg = MeiElement('reg')
	staffGrp_reg = MeiElement('staffGrp')
	# Give reg staffGrp all the attributes of the orig one
	for attr in staffGrp_orig.getChildren():
		staffGrp_reg.addAttribute(attr.getName(), attr.getValue())
	# Add new elements in appropriate hierarchy
	choice.addChild(orig)
	choice.addChild(reg)
	orig.addChild(staffGrp_orig)
	reg.addChild(staffGrp_reg)
	for staffDef in staffGrp_orig.getChildren():
		staffGrp_reg.addChild(regularize_clef(staffDef))
	return choice

def regularize_clef(staffDef_orig):
	"""Produces a single staffDef with a regularized clef
	based on a staffDef with an original clef.
	"""
	staffDef_reg = MeiElement('staffDef')
	# First, get clef information and use that to add regularized clefs
	# Save o_clef (original clef) as tuple, e.g. ('C', '3')
	o_clef = (staffDef_orig.getAttribute('clef.shape').getValue(),
	          staffDef_orig.getAttribute('clef.line').getValue())
	# subbass, bass, baritone all become F4.
	if o_clef == ('C', '5') or o_clef[0] == 'F':
		staffDef_reg.addAttribute('clef.shape', 'F')
		staffDef_reg.addAttribute('clef.line', '4')
	# tenor, alto become 8vb-transposing G2.
	elif o_clef == ('C', '3') or o_clef == ('C', '4'):
		staffDef_reg.addAttribute('clef.shape', 'G')
		staffDef_reg.addAttribute('clef.line', '2')
		staffDef_reg.addAttribute('clef.dis', '8')
		staffDef_reg.addAttribute('clef.dis.place', 'below')
	# treble, soprano, mezzo-soprano become G2.
	else:
		staffDef_reg.addAttribute('clef.shape', 'G')
		staffDef_reg.addAttribute('clef.line', '2')
	# Then, add all the other attributes of the staffDef intact
	for attr in staffDef_orig.getAttributes():
		if 'clef.' not in attr.getName():
			staffDef_reg.addAttribute(attr.getName(), attr.getValue())
	return staffDef_reg

def orig_clefs_choice(staffGrp_reg, orig_clefs):
	"""Returns <choice> tag with a <reg> and an <orig>.
	The <reg> tag contains the <staffGrp> of regularized
	clefs that was already there. The <orig> tag contains
	the original clefs, which are provided as a parameter
	in the form of a tuple of strings.
	Compare reg_clefs_choice.
	"""
	# Create new MEI elements
	choice = pymei.createInstance('choice')
	orig = pymei.createInstance('orig')
	reg = pymei.createInstance('reg')
	staffGrp_orig = pymei.createInstance('staffGrp')
	# Give orig staffGrp all the attributes of the reg one
	for attr in staffGrp_reg.getAttributes():
		staffGrp_orig.addAttribute(attr.getName(), attr.getValue())
	# Add new elements in appropriate hierarchy
	choice.addChild(orig)
	choice.addChild(reg)
	reg.addChild(staffGrp_reg)
	orig.addChild(staffGrp_orig)
	for staffDef in staffGrp_reg.getChildren():
		staffGrp_orig.addChild()
	return choice

def normalize(clef_group):
	"""Makes sure clefs are in correct format, such as 'C3'."""
	try:
		assert len(clef_group) == 4
		if clef_group == EMPTY_CLEFS:
			return clef_group
		for i in range(len(clef_group)):
			clef_group[i] = clef_group[i].replace(' ', '')
			assert len(clef_group[i] == 2)
			assert (clef_group[i][0] in CLEF_SHAPES or
			        clef_group[i][1] in CLEF_SHAPES)
			# Swap if the order of line and shape are reversed (e.g. '3C')
			if clef_group[i][1] in CLEF_SHAPES:
				clef_group[i] = clef_group[i][1] + clef_group[i][0]
			# There must be a digit indicating the line of the clef
			assert clef_group[i][1] in POSSIBLE_LINES
			# Make sure it's uppercase
			clef_group[i] = clef_group[i][0].upper() + clef_group[i][1]
		return clef_group
	except AssertionError or IndexError:
		print("The clef information provided is invalid. "
		      "Original clefs will not be provided.")
		return EMPTY_CLEFS

def clefs(MEI_tree, orig_clefs):
	"""Finds the clefs in a document, adds regularized clefs
	if appropriate, and adds original clefs if provided.
	"""
	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	for staffGrp in all_staffGrp:
		# Only operate if not part of <orig> or <reg> to begin with
		if staffGrp.getParent().getName() not in [ORIG, REG]:
			if has_C_clef(staffGrp):
				parent = staffGrp.getParent()
				parent.addChild(reg_clefs_choice(staffGrp))
				parent.removeChild(staffGrp)
			elif normalize(orig_clefs) != EMPTY_CLEFS:
				parent = staffGrp.getParent()
				parent.addChild(orig_clefs_choice(staffGrp, orig_clefs))
				parent.removeChild(staffGrp)
			else:
				pass


