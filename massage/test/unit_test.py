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

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UtilitiesTest, 'test'))
    return test_suite
