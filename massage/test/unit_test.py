import sys
import unittest
sys.path.insert(0, '..')

from pymei import MeiElement, MeiAttribute, XmlImport, XmlExport
import utilities
from analyze.analyze import analyze

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

class AnalysisTest(unittest.TestCase):
    
    def test_analyze(self):
        analysis = analyze('../test/dat/DC0909E.mei')
        
        self.assertEqual(True, analysis.first_measure_empty)
        self.assertEqual(False, analysis.has_editor_element)
        self.assertEqual(False, analysis.has_arranger_element)
        self.assertEqual('', analysis.editor_name)
        self.assertListEqual(analysis.staff_list,
            [('Superius', 'Superius', 'variant', '', '1'), 
             ('Superius_Variant_1554/22', 'Superius', 'variant', 'RISM1554-22', '2'), 
             ('Contratenor', 'Contratenor', 'variant', '', '3'), 
             ('Contratenor_Emendation_Tanguy', 'Contratenor', 'emendation', 'Tanguy', '4'), 
             ('Contratenor_Variant_1554/22', 'Contratenor', 'variant', 'RISM1554-22', '5'), 
             ('Tenor', 'Tenor', 'variant', '', '6'), 
             ('Tenor_Variant_1554/22', 'Tenor', 'variant', 'RISM1554-22', '7'), 
             ('Bassus', 'Bassus', 'variant', '', '8'), 
             ('Bassus_Variant_1554/22', 'Bassus', 'variant', 'RISM1554-22', '9'),
        ])
        self.assertListEqual(analysis.alternates_list,
            [('1', 'variant', '1', ''), 
             ('2', 'variant', '1', 'RISM1554-22'), 
             ('3', 'variant', '3', ''), 
             ('4', 'emendation', '3', 'Tanguy'), 
             ('5', 'variant', '3', 'RISM1554-22'), 
             ('6', 'variant', '6', ''), 
             ('7', 'variant', '6', 'RISM1554-22'), 
             ('8', 'variant', '8', ''), 
             ('9', 'variant', '8', 'RISM1554-22'),
        ])

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UtilitiesTest, 'test'))
    test_suite.addTest(unittest.makeSuite(AnalysisTest, 'test'))
    return test_suite
    
if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
