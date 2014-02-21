import sys
import unittest
sys.path.insert(0, '..')

from transform.transform import TransformData
from transformtestrunner import TransformTestCase
from constants import *
from transform.alt import *

class FunctionTest(unittest.TestCase):
			
	def test_dur_in_semibreves_notes(self):
		section = MeiElement('score')

		m1 = MeiElement('measure')
		st1 = MeiElement('staff')
		ly1 = MeiElement('layer')
		nt1 = MeiElement('note')
		nt2 = MeiElement('note')
		nt3 = MeiElement('note')
		nt4 = MeiElement('note')
		nt5 = MeiElement('note')
		nt6 = MeiElement('note')
		nt7 = MeiElement('note')
		nt8 = MeiElement('note')
		nt9 = MeiElement('note')
		nt1.addAttribute('dur', '1')
		nt2.addAttribute('dur', '2')
		nt3.addAttribute('dur', '4')
		nt4.addAttribute('dur', '8')
		nt5.addAttribute('dur', '16')
		nt6.addAttribute('dur', '32')
		nt7.addAttribute('dur', '64')
		nt8.addAttribute('dur', 'long')
		nt9.addAttribute('dur', 'breve')
		
		self.assertEqual(dur_in_semibreves(nt1), 1)
		self.assertEqual(dur_in_semibreves(nt2), 1/2)
		self.assertEqual(dur_in_semibreves(nt3), 1/4)
		self.assertEqual(dur_in_semibreves(nt4), 1/8)
		self.assertEqual(dur_in_semibreves(nt5), 1/16)
		self.assertEqual(dur_in_semibreves(nt6), 1/32)
		self.assertEqual(dur_in_semibreves(nt7), 1/64)
		self.assertEqual(dur_in_semibreves(nt8), 2)
		self.assertEqual(dur_in_semibreves(nt9), 4)

	def test_dur_in_semibreves_mRests(self):
		sctn = MeiElement('score')
		scD1 = MeiElement('scoreDef')
		scD2 = MeiElement('scoreDef')
		srG1 = MeiElement('staffGrp')
		srG2 = MeiElement('staffGrp')
		stD1 = MeiElement('staffDef')
		stD2 = MeiElement('staffDef')

		m1 = MeiElement('measure')
		m2 = MeiElement('measure')
		l1 = MeiElement('layer')
		l2 = MeiElement('layer')
		s1 = MeiElement('staff')
		s2 = MeiElement('staff')

		mR1 = MeiElement('mRest')
		mR2 = MeiElement('mRest')
		
		scD1.addAttribute('meter.unit', '2')
		stD1.addAttribute('meter.count', '2')
		stD2.addAttribute('meter.count', '3')
		
		st1.addAttribute('n', '1')
		
		sctn.addChild(scD1)
		scD1.addChild(stG1)
		stG1.addChild(stD1)
		sctn.addChild(m1)
		m1.addChild(l1)
		l1.addChild(s1)
		s1.addChild(mR1)

		sctn.addChild(scD2)
		scD2.addChild(stG2)
		stG2.addChild(stD2)
		sctn.addChild(m2)
		m2.addChild(l2)
		l2.addChild(s2)
		s2.addChild(mR2)

		self.assertEqual(dur_in_semibreves(mR1), 1)
		self.assertEqual(dur_in_semibreves(mR2), 1.5)
		

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
    
if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
