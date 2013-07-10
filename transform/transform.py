import clefs
import arranger
from constants import *
from pymei import XmlImport, XmlExport

class TransformData:
	def __init__(self, orig_clefs=EMPTY_CLEFS, arranger_editor=False):
		self.orig_clefs = orig_clefs

def TEST_SET_UP(data):
	"""Mutates data to test specific transformations"""
	data.arranger_editor = True

def transform(MEI_doc, data=TransformData()):
	new_doc = MEI_doc
	tree = new_doc.getRootElement()
	clefs.clefs(tree, data.orig_clefs)
	arranger.arranger(tree, data.arranger_editor)
	return new_doc

def ui():
	old_filename = raw_input("Filename to transform: ")
	if '.mei' not in old_filename or old_filename[-4:] != '.mei':
		old_filename += '.mei'
	old_MEI_doc = XmlImport.documentFromFile(old_filename)
	data = TransformData() # Will be filled in
	TEST_SET_UP(data) # For testing purposes
	new_MEI_doc = transform(old_MEI_doc, data)
	new_filename = old_filename[:-4] + '_.mei'
	status = XmlExport.meiDocumentToFile(new_MEI_doc, new_filename)
	if status:
		print("Transformed file saved as " + new_filename)
	else:
		print("Transformation failed")

if __name__ == "__main__":
	ui()
