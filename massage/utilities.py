
def has_C_clef(staffGrp):
	for staffDef in staffGrp.getChildren():
		if staffDef.getAttribute('clef.shape').getValue() == 'C':
			return True
	return False

def get_all_staves(MEI_tree):
	return MEI_tree.getDescendantsByName('staff')
