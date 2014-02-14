import sys
import unittest
sys.path.insert(0, '..')

from transform.transform import TransformData
from transformtestrunner import TransformTestCase
from constants import *

class TransformTest(unittest.TestCase):
	
	def setUp(self):
		pass

	def test_incipit_noincipit(self):
		name = 'TC_Incipit.01 - No incipit measure'
		mei_file = 'dat/TC.Incip.None.mei'
		transform_data = TransformData()
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '2', ''),
				('3', VARIANT, '3', ''),
				('4', VARIANT, '4', ''),
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_incipit_simple(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_incipit_extrastavesandincipit(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_variants_one(self):
		name = 'TC_Variants.00 - One variant source'
		mei_file = 'dat/TC.Variants.00.mei'
		transform_data = TransformData()
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '1', 'SourceA 1552/01'),
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_variants_threesources(self):
		name = 'TC_Variants.01'
		mei_file = 'dat/TC.Variants.01.mei'
		transform_data = TransformData()
		transform_data.arranger_to_editor = True
		transform_data.replace_longa = False
		transform_data.obliterate_incipit = False
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '1', '2014/01'),
				('3', VARIANT, '1', '0001/01'),
				('4', VARIANT, '1', 'ZK 0001/00'), 
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_variants_wholemeasureapps(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_variants_multipleblocks(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei


	def test_emendations_01(self):
		name = 'TC_Emendations.01'
		mei_file = 'dat/TC.Emendations.01.mei'
		transform_data = TransformData()
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', EMENDATION, '1', 'ZK'),
				('3', EMENDATION, '1', 'ZK'),
				('4', EMENDATION, '1', 'ZK'), 
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_reconstructions_tworeconstructedvoices(self):
		name = 'TC_Reconstructions.01 - Two reconstructed voices'
		mei_file = 'dat/TC.Reconstructions.01.mei'
		transform_data = TransformData()
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '2', ''),
				('3', RECONSTRUCTION, '2', 'EditorX'),
				('4', RECONSTRUCTION, '2', 'EditorY'), 
				('5', VARIANT, '5', ''),
				('6', RECONSTRUCTION, '5', 'EditorX'), 
				('7', RECONSTRUCTION, '5', 'EditorY'),
				('8', VARIANT, '8', '')
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_canonical_01(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_canonical_colors(self):
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
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei

	def test_canonical_reconvariantforsamevoice(self):
		name = 'MasterPlainMEI.03 - recon+variant for the same voice'
		mei_file = 'dat/TC.MasterPlainMEI.03.mei'
		transform_data = TransformData()
		transform_data.arranger_to_editor = True
		transform_data.replace_longa = False
		transform_data.obliterate_incipit = False
		transform_data.editorial_resp = 'ZK'
		transform_data.alternates_list = [
				('1', VARIANT, '1', ''),
				('2', VARIANT, '2', ''),
				('3', VARIANT, '3', ''),
				('4', VARIANT, '3', 'RISM1560-6'),
				('5', RECONSTRUCTION, '2', 'Contributor-A'),
				('6', RECONSTRUCTION, '2', 'Contributor-B'), 
				('7', VARIANT, '7', ''),
				('8', EMENDATION, '7', 'Komives'), 
				('9', VARIANT, '9', ''),
				]
		transformed_mei = TransformTestCase(name, mei_file, transform_data).Run()
		# TODO: do some asserts	on transformed_mei


def suite():
	test_suite = unittest.TestSuite()
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_incipit_noincipit'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_incipit_simple'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_incipit_extrastavesandincipit'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_variants_one'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_variants_threesources'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_variants_wholemeasureapps'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_variants_multipleblocks'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_emendations_01'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_reconstructions_tworeconstructedvoices'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_canonical_01'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_canonical_colors'))
	test_suite.addTest(unittest.TestLoader().loadTestsFromName('transform_test.TransformTest.test_canonical_reconvariantforsamevoice'))
	return test_suite
    
# for tc in test_cases:
# 	if tc.name in to_run:
# 		tc.Run()

# 
