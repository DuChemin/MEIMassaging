import sys
import argparse
import unittest
sys.path.insert(0, '..')

from transform.transform import TransformData
from transformtestrunner import TransformTestCase
from constants import *
from transform.alt import *
from pymei import MeiElement, MeiDocument, MeiAttribute
import utilities

class FunctionTest(unittest.TestCase):
	
	def test_linkalternatives_connecting(self):
		"""need apps that are connected
		i.e.:
		  1. they are in subsequent measures, 
		  2. they are on the same staff,
		  3. there isn't any notes or rests are in between them and
		  4. their rdgs represent the exact same set of sources
		Apps need to have xml:id. Only apps lower than <staff> level 
		will be linked together.
		"""

		music = MeiElement('music')
		body = MeiElement('body')
		mdiv = MeiElement('mdiv')
		score = MeiElement('score')
		section = MeiElement('section')
		m1 = MeiElement('measure')
		m2 = MeiElement('measure')
		m3 = MeiElement('measure')
		s1 = MeiElement('staff')
		s2 = MeiElement('staff')
		s3 = MeiElement('staff')
		s3.addAttribute('n', '2')

		app1 = MeiElement('app')
		app2 = MeiElement('app')
		app3 = MeiElement('app')
		lem1 = MeiElement('lem')
		lem2 = MeiElement('lem')
		lem3 = MeiElement('lem')
		rdg1_A = MeiElement('rdg')
		rdg1_B = MeiElement('rdg')
		rdg2_A = MeiElement('rdg')
		rdg2_B = MeiElement('rdg')
		rdg1_A.addAttribute('source', "SRC-A")
		rdg1_B.addAttribute('source', "SRC-B")
		rdg2_A.addAttribute('source', "SRC-A")
		rdg2_B.addAttribute('source', "SRC-B")

		music.addChild(body)
		body.addChild(mdiv)
		mdiv.addChild(score)
		score.addChild(section)
		section.addChild(m1)
		m1.addChild(s1)
		section.addChild(m2)
		m2.addChild(s2)

		"""
		app1 and app2 are connecting apps in m1 and m2
		"""
		s1.addChild(app1)
		app1.addChild(lem1)
		app1.addChild(rdg1_A)
		app1.addChild(rdg1_B)
		
		s2.addChild(app2)
		app2.addChild(lem2)
		app2.addChild(rdg2_A)
		app2.addChild(rdg2_B)

		link_alternatives(music)
		
		""""
		This is to establish that the connecting apps
		are linked together:
		"""
		annots = get_descendants(music, 'annot[type=appGrp]')
		self.assertEqual(len(annots), 2)
		self.assertEqual(annots[0].hasAttribute('plist'), True)
		plist = annots[0].getAttribute('plist').getValue()
		appIDs = plist.split(',')
		self.assertEqual(len(appIDs), 2)
		self.assertEqual(appIds[0], "#" + app1.getId())
		self.assertEqual(appIds[1], "#" + app2.getId())
		
		
	def test_linkalternatives_nonconnecting(self):
		"""need apps that are connected
		(i.e.:
		  1. they are in subsequent measures and no 
		     more notes or rests are in between them.
		  2. their rdgs have the exact same set of sources)
		Apps need to have xml:id

		This test is asserts whether some subsequent apps
		that have different set of sources do not get linked
		together.
		"""
		music = MeiElement('music')
		body = MeiElement('body')
		mdiv = MeiElement('mdiv')
		score = MeiElement('score')
		section = MeiElement('section')
		m1 = MeiElement('measure')
		m2 = MeiElement('measure')
		m3 = MeiElement('measure')
		s1 = MeiElement('staff')
		s2 = MeiElement('staff')
		s3_1 = MeiElement('staff')
		s3_2 = MeiElement('staff')
		s3_1.addAttribute('n', '1')
		s3_2.addAttribute('n', '2')

		app1 = MeiElement('app')
		app2 = MeiElement('app')
		app3_1 = MeiElement('app')
		app3_2 = MeiElement('app')
		app3_3 = MeiElement('app')
		lem1 = MeiElement('lem')
		lem2 = MeiElement('lem')
		lem3_1 = MeiElement('lem')
		lem3_2 = MeiElement('lem')
		lem3_3 = MeiElement('lem')
		rdg1_A = MeiElement('rdg')
		rdg1_B = MeiElement('rdg')
		rdg2_A = MeiElement('rdg')
		rdg2_B = MeiElement('rdg')
		rdg3_1_A = MeiElement('rdg')
		rdg3_1_C = MeiElement('rdg')
		rdg3_2_A = MeiElement('rdg')
		rdg3_2_B = MeiElement('rdg')
		rdg3_3_A = MeiElement('rdg')
		rdg3_3_B = MeiElement('rdg')
		rdg1_A.addAttribute('source', "SRC-A")
		rdg1_B.addAttribute('source', "SRC-B")
		rdg2_A.addAttribute('source', "SRC-A")
		rdg2_B.addAttribute('source', "SRC-B")
		rdg3_1_A.addAttribute('source', "SRC-A")
		rdg3_1_C.addAttribute('source', "SRC-C")
		rdg3_2_A.addAttribute('source', "SRC-A")
		rdg3_2_B.addAttribute('source', "SRC-B")
		rdg3_3_A.addAttribute('source', "SRC-A")
		rdg3_3_B.addAttribute('source', "SRC-B")

		music.addChild(body)
		body.addChild(mdiv)
		mdiv.addChild(score)
		score.addChild(section)
		section.addChild(m1)
		m1.addChild(s1)
		section.addChild(m2)
		m2.addChild(s2)
		section.addChild(m3)
		m3.addChild(s3_1)
		m3.addChild(s3_2)

		s1.addChild(app1)
		app1.addChild(lem1)
		app1.addChild(rdg1_A)
		app1.addChild(rdg1_B)

		"""app1 doesn't connect with app2 because there's 
		a note between the two"""
		l2 = MeiElement('layer')
		s2.addChild(l2)
		l2.addChild(MeiElement('note'))
		l2.addChild(app2)
		app2.addChild(lem2)
		app2.addChild(rdg2_A)
		app2.addChild(rdg2_B)

		"""app3_1 doesn't connect with app2 because it
		has a different set of sources"""
		s3_1.addChild(app3_1)
		app3_1.addChild(lem3_1)
		app3_1.addChild(rdg3_1_A)
		app3_1.addChild(rdg3_1_C)

		"""app3_2 doesn't connect with app2 because it is
		on a different staff"""
		s3_2.addChild(app3_2)
		app3_2.addChild(lem3_2)
		app3_2.addChild(rdg3_2_A)
		app3_2.addChild(rdg3_2_B)

		"""app3_3 doesn't connect with app2 because it is
		at a higher level (not descendant of staff)"""
		m3.addChild(app3_3)
		app3_3.addChild(lem3_3)
		app3_3.addChild(rdg3_3_A)
		app3_3.addChild(rdg3_3_B)

		link_alternatives(music)
		
		""""
		This is to establish that the non-connecting apps
		aren't linked together:
		"""
		annots = get_descendants(music, 'annot[type=appGrp]')
		self.assertEqual(len(annots), 0)
		
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
	test_suite.addTest(unittest.makeSuite(FunctionTest, 'test'))
	return test_suite
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MEI-Massage a single file.')
    utilities.set_logging(parser)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
