import sys
import unittest
sys.path.insert(0, '..')

from transform.transform import TransformData
from transformtestrunner import TransformTestCase
from constants import *

class DuCheminTest(unittest.TestCase):
	def setUp(self):
		pass

	def test_emendations_DC0113(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_reconstructions_DC1209(self):
		name = 'TC_Reconstructions.DC1209'
		mei_file = 'dat/DC1209E.mei'
		transform_data = TransformData()
		transform_data.arranger_to_editor = True
		transform_data.replace_longa = True
		transform_data.obliterate_incipit = True
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '2', ''),
				('3', RECONSTRUCTION, '2', 'Apgar'),
				('4', RECONSTRUCTION, '2', 'Busnel'),
				('5', RECONSTRUCTION, '2', 'Freedman'),
				('6', VARIANT, '6', ''), 
				('7', VARIANT, '7', ''), 
				('8', RECONSTRUCTION, '7', 'Apgar'),
				('9', RECONSTRUCTION, '7', 'Busnel'),
				('10', RECONSTRUCTION, '7', 'Freedman'),
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_reconstructions_DC1313(self):
		name = 'TC_Reconstructions.DC1313'
		mei_file = 'dat/DC1313E.mei'
		transform_data = TransformData()
		transform_data.arranger_to_editor = True
		transform_data.replace_longa = True
		transform_data.obliterate_incipit = True
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '2', ''),
				('3', RECONSTRUCTION, '2', 'Apgar'),
				('4', RECONSTRUCTION, '2', 'Bruke'),
				('5', RECONSTRUCTION, '2', 'Derycz'),
				('6', RECONSTRUCTION, '2', 'Freedman'),
				('7', VARIANT, '7', ''), 
				('8', VARIANT, '8', ''), 
				('9', RECONSTRUCTION, '8', 'Apgar'),
				('10', RECONSTRUCTION, '8', 'Bruke'),
				('11', RECONSTRUCTION, '8', 'Derycz'),
				('12', RECONSTRUCTION, '8', 'Freedman'),
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_variants_DC0221(self):
		name = 'TC_DC0221'
		mei_file = 'dat/DC0221E.mei'
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
				('7', VARIANT, '7', ''),
				('8', VARIANT, '7', 'ZK'),
				('9', VARIANT, '7', 'ZK'),
				('10', VARIANT, '10', ''),
				('11', VARIANT, '10', 'ZK'),
				('12', VARIANT, '10', 'ZK') ]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromName('dc_test.DuCheminTest.test_emendations_DC0113'))
    test_suite.addTest(unittest.TestLoader().loadTestsFromName('dc_test.DuCheminTest.test_reconstructions_DC1209'))
    test_suite.addTest(unittest.TestLoader().loadTestsFromName('dc_test.DuCheminTest.test_reconstructions_DC1313'))
    test_suite.addTest(unittest.TestLoader().loadTestsFromName('dc_test.DuCheminTest.test_variants_DC0221'))
    return test_suite
