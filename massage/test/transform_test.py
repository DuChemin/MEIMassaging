import sys
sys.path.insert(0, '..')

from transform.transform import *
from pymei import XmlImport, XmlExport

test_cases = [] 

class TestCase:
	def __init__(self,name,mei_file,transform_data,outsuffix='_'):
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
		print('running test case ' + self.name + ' Input: ' + old_filename)
		#running the test:
		new_MEI_doc = transform(old_MEI_doc, self.transform_data)
		new_filename = (old_filename[:-EXT_LENGTH] + self.outsuffix + '_' +
				old_filename[-EXT_LENGTH:])
		status = XmlExport.meiDocumentToFile(new_MEI_doc, new_filename)
		if status:
			print("Done. Transformed file saved as " + new_filename)
		else:
			print("Transformation failed")

""" =========================================="""
""" ========== SIMPLE TEST CASES ============= """

name = 'TC_Incipit.01 - No incipit measure'
mei_file = 'dat/TC.Incip.None.mei'
transform_data = TransformData()
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', VARIANT, '3', ''),
		('4', VARIANT, '4', ''),
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_Incipit.02 - Simple MEI with incipit'
mei_file = 'dat/TC.Incip.Simple.mei'
transform_data = TransformData()
transform_data.obliterate_incipit = True
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', VARIANT, '3', ''),
		('4', VARIANT, '4', ''),
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_Incipit.03 - MEI with extra staves and incipit'
mei_file = 'dat/TC.Incip.ExtraStaves.mei'
transform_data = TransformData()
transform_data.obliterate_incipit = True
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', RECONSTRUCTION, '4', 'KZ'),
		('4', VARIANT, '4', ''),
		('5', VARIANT, '5', ''),
		('6', EMENDATION, '5', 'KZ'),
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_Variants.01'
mei_file = 'dat/TC.Variants.01.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = False
transform_data.obliterate_incipit = False
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '1', 'ZK'),
		('3', VARIANT, '1', 'ZK'),
		('4', VARIANT, '1', 'ZK'), 
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_Variants.02 - Whole-Measure <app>'
mei_file = 'dat/TC.Variants.02.WholeMeasure.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = False
transform_data.obliterate_incipit = False
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '1', 'ZK'),
		('3', VARIANT, '1', 'ZK') 
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_Variants.03 - Multiple colored blocks'
mei_file = 'dat/TC.Variants.03.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = False
transform_data.obliterate_incipit = False
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '1', 'ZK'),
		('3', VARIANT, '1', 'ZK') 
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'MasterPlainMEI.01 - All-in-one'
mei_file = 'dat/TC.MasterPlainMEI.01.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = False
transform_data.obliterate_incipit = False
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', RECONSTRUCTION, '2', 'Contributor-A'),
		('4', RECONSTRUCTION, '2', 'Contributor-B'), 
		('5', VARIANT, '5', ''),
		('6', EMENDATION, '5', 'Komives'), 
		('7', VARIANT, '7', ''),
		('8', VARIANT, '7', 'Source-A'), 
		]
test_cases.append(TestCase(name, mei_file, transform_data))

name = 'MasterPlainMEI.02 - Colors Specified'
mei_file = 'dat/TC.MasterPlainMEI.02.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = False
transform_data.obliterate_incipit = False
transform_data.editorial_resp = 'ZK'
transform_data.color_for_variants = BLUE
transform_data.color_for_emendations = GREEN
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '1', 'ZK'),
		('3', EMENDATION, '1', 'ZK') 
		]
test_cases.append(TestCase(name, mei_file, transform_data))

""" =========================================="""
""" ========== DU CHEMIN TEST FILES ========== """

name = 'TC_Emendations.DC0113'
mei_file = 'dat/DC0113E.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = True
transform_data.obliterate_incipit = True
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', EMENDATION, '2', 'Freedman'),
		('4', VARIANT, '4', ''),
		('5', VARIANT, '5', ''), 
		('6', EMENDATION, '5', 'Freedman'), 
		]
# test_cases.append(TestCase(name, mei_file, transform_data))


name = 'TC_Reconstructions.DC1209'
mei_file = 'dat/DC1209_Synoptic_Reconstruction-normalized.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = True
transform_data.obliterate_incipit = False
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', RECONSTRUCTION, '2', 'ZK'),
		('4', RECONSTRUCTION, '2', 'ZK'),
		('5', VARIANT, '5', ''), 
		('6', VARIANT, '6', ''), 
		('7', RECONSTRUCTION, '6', 'ZK'),
		('8', RECONSTRUCTION, '6', 'ZK'),
		]
# test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_Reconstructions.DC1313'
mei_file = 'dat/DC1313_Synoptic_Reconstruction-normalized.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = True
transform_data.obliterate_incipit = True
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '2', ''),
		('3', RECONSTRUCTION, '2', 'ZK'),
		('4', RECONSTRUCTION, '2', 'ZK'),
		('5', VARIANT, '5', ''), 
		('6', VARIANT, '6', ''), 
		('7', RECONSTRUCTION, '6', 'ZK'),
		('8', RECONSTRUCTION, '6', 'ZK'),
		]
# test_cases.append(TestCase(name, mei_file, transform_data))

name = 'TC_DC0221'
mei_file = 'dat/DC0221_Synoptic_Variants.Voice_Type_Source.mei'
transform_data = TransformData()
transform_data.arranger_to_editor = True
transform_data.replace_longa = True
transform_data.obliterate_incipit = True
transform_data.editorial_resp = 'ZK'
transform_data.alternates_list = [
		('1', VARIANT, '1', ''),
		('2', VARIANT, '1', 'ZK'),
		('3', VARIANT, '1', 'ZK'),
		('4', VARIANT, '4', ''),
		('5', VARIANT, '4', 'ZK'),
		('6', VARIANT, '4', 'ZK'),
		('7', VARIANT, '4', 'ZK'),
		('8', VARIANT, '8', ''),
		('9', VARIANT, '8', 'ZK'),
		('10', VARIANT, '8', 'ZK'),
		('11', VARIANT, '11', ''),
		('12', VARIANT, '11', 'ZK'),
		('13', VARIANT, '11', 'ZK') ]
#test_cases.append(TestCase(name, mei_file, transform_data))

to_run = []
to_run.append('TC_Incipit.01 - No incipit measure')
to_run.append('TC_Incipit.02 - Simple MEI with incipit')
to_run.append('TC_Incipit.03 - MEI with extra staves and incipit')

for tc in test_cases:
	if tc.name in to_run:
		tc.Run()

