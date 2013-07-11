
def has_C_clef(staffGrp):
	for staffDef in staffGrp.getChildren():
		if staffDef.getAttribute('clef.shape').getValue() == 'C':
			return True
	return False