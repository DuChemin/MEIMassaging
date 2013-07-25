
def has_C_clef(staffGrp):
	for staffDef in staffGrp.getChildren():
		if staffDef.getAttribute('clef.shape').getValue() == 'C':
			return True
	return False

def add_export_suffix(file_path):
	return file_path.replace('.mei', '_new.mei')