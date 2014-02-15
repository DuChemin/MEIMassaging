import sys
sys.path.insert(0, '..')

from transform.transform import *
from pymei import XmlImport, XmlExport

class TransformTestCase:
	def __init__(self,name,mei_file,transform_data,outsuffix=''):
		self.name = name
		self.mei_file = mei_file
		self.transform_data = transform_data
		self.outsuffix = outsuffix

	def Run(self):
		old_filename = self.mei_file
		if (len(old_filename) < EXT_LENGTH or
				old_filename[-EXT_LENGTH:] not in EXT):
			print("No file extension provided; " + EXT[0] + " used.")
			old_filename += EXT[0]
		old_MEI_doc = XmlImport.documentFromFile(old_filename)
		# print('running test case ' + self.name + ' Input: ' + old_filename)
		new_MEI_doc = transform(old_MEI_doc, self.transform_data)
		new_filename = (old_filename[:-EXT_LENGTH] + self.outsuffix + '_' +
				old_filename[-EXT_LENGTH:])
		status = XmlExport.meiDocumentToFile(new_MEI_doc, new_filename)
		if status:
			# print("Done. Transformed file saved as " + new_filename)
			pass
		else:
			print("Transformation failed")