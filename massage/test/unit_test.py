import sys
import unittest
sys.path.insert(0, '..')

from pymei import MeiElement, MeiAttribute, XmlImport, XmlExport
import utilities
from transform.transform import *

class UtilitiesTest(unittest.TestCase):
	
	def test_get_descendants(self):
		
		measure = MeiElement('measure')
		layer = MeiElement('layer')
		note1 = MeiElement('note')
		note2 = MeiElement('note')
		note3 = MeiElement('note')
		rest1 = MeiElement('rest')
		rest2 = MeiElement('rest')
		
		note1.addAttribute('pname', 'c')
		note2.addAttribute('pname', 'd')
		note2.addAttribute('dur', '1')
		note3.addAttribute('pname', 'd')
		note3.addAttribute('dur', '2')
		rest1.addAttribute('dur', '1')
		rest2.addAttribute('dur', '2')
		
		layer.addChild(note1)
		layer.addChild(note2)
		layer.addChild(note3)
		layer.addChild(rest1)
		layer.addChild(rest2)
		measure.addChild(layer)
		
		self.assertEqual(3, len(utilities.get_descendants(measure, 'note')))
		self.assertEqual(5, len(utilities.get_descendants(measure, 'note rest')))
		self.assertEqual(1, len(utilities.get_descendants(measure, 'note[dur=1]')))
		self.assertEqual(4, len(utilities.get_descendants(measure, 'note[dur=1] note[pname=c] rest[dur=2] layer')))



# class TransformTest(unittest.TestCase):
# 
# 	class TestCase:
# 		def __init__(self,name,mei_file,transform_data,outsuffix=''):
# 			self.name = name
# 			self.mei_file = mei_file
# 			self.transform_data = transform_data
# 			self.outsuffix = outsuffix
# 
# 		def Run(self):
# 			old_filename = self.mei_file
# 			if (len(old_filename) < EXT_LENGTH or
# 					old_filename[-EXT_LENGTH:] not in EXT):
# 				print("No file extension provided; " + EXT[0] + " used.")
# 				old_filename += EXT[0]
# 			old_MEI_doc = XmlImport.documentFromFile(old_filename)
# 			print('running test case ' + self.name + ' Input: ' + old_filename)
# 			#running the test:
# 			new_MEI_doc = transform(old_MEI_doc, self.transform_data)
# 			new_filename = (old_filename[:-EXT_LENGTH] + self.outsuffix + '_' +
# 					old_filename[-EXT_LENGTH:])
# 			status = XmlExport.meiDocumentToFile(new_MEI_doc, new_filename)
# 			if status:
# 				print("Done. Transformed file saved as " + new_filename)
# 			else:
# 				print("Transformation failed")	
# 
# 	def test_incipit_none(self):
# 		name = 'TC_Incipit.01 - No incipit measure'
# 		mei_file = 'dat/TC.Incip.None.mei'
# 		transform_data = TransformData()
# 		transform_data.alternates_list = [
# 				('1', VARIANT, '1', ''),
# 				('2', VARIANT, '2', ''),
# 				('3', VARIANT, '3', ''),
# 				('4', VARIANT, '4', ''),
# 				]
# 		test_case = TransformTest.TestCase(name, mei_file, transform_data)
# 		transformed_mei = test_case.Run()
# 		# TODO: do some asserts	on transformed_mei
# 	
# 	def test_incipit_simple(self):
# 		name = 'TC_Incipit.02 - Simple MEI with incipit'
# 		mei_file = 'dat/TC.Incip.Simple.mei'
# 		transform_data = TransformData()
# 		transform_data.obliterate_incipit = True
# 		transform_data.alternates_list = [
# 				('1', VARIANT, '1', ''),
# 				('2', VARIANT, '2', ''),
# 				('3', VARIANT, '3', ''),
# 				('4', VARIANT, '4', ''),
# 				]
# 		test_case = TransformTest.TestCase(name, mei_file, transform_data)
# 		transformed_mei = test_case.Run()
# 		# TODO: do some asserts	on transformed_mei
# 
# 	def test_incipit_extrastaves(self):
# 		name = 'TC_Incipit.03 - MEI with extra staves and incipit'
# 		mei_file = 'dat/TC.Incip.ExtraStaves.mei'
# 		transform_data = TransformData()
# 		transform_data.obliterate_incipit = True
# 		transform_data.alternates_list = [
# 				('1', VARIANT, '1', ''),
# 				('2', VARIANT, '2', ''),
# 				('3', RECONSTRUCTION, '4', 'KZ'),
# 				('4', VARIANT, '4', ''),
# 				('5', VARIANT, '5', ''),
# 				('6', EMENDATION, '5', 'KZ'),
# 				]
# 		test_case = TransformTest.TestCase(name, mei_file, transform_data)
# 		transformed_mei = test_case.Run()
# 		# TODO: do some asserts	on transformed_mei

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UtilitiesTest, 'test'))

		#TODO: when a test case causes segmentation fault, the whole test suite would abort.
		# until we solve the segfault issue, there's no point to run all test cases here. 
		# in transform_test.py we can simly comment out one line to avoide running segfaulting test cases, 
		# so until the segfault issue is solved use transform_test.py!
    # test_suite.addTest(unittest.makeSuite(TransformTest, 'test'))
    return test_suite
    
runner = unittest.TextTestRunner()
runner.run(suite())
