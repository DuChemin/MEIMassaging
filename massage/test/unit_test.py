import sys
import argparse
import unittest
sys.path.insert(0, '..')

from pymei import MeiElement, MeiAttribute, XmlImport, XmlExport, MeiDocument
import utilities
from analyze.analyze import analyze

class UtilitiesTest(unittest.TestCase):

    def test_get_descendants(self):

        measure = MeiElement('measure')
        layer   = MeiElement('layer')
        note1   = MeiElement('note')
        note2   = MeiElement('note')
        note3   = MeiElement('note')
        rest1   = MeiElement('rest')
        rest2   = MeiElement('rest')

        note1.addAttribute('pname', 'c')
        note1.addAttribute('oct', '4')
        note1.addAttribute('dur', 'breve')
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
        self.assertEqual(1, len(utilities.get_descendants(measure, 'note[pname=d,dur=1]')))
        self.assertEqual(4, len(utilities.get_descendants(measure, 'note[pname=d,dur=1] note[pname=c,oct=4,dur=breve] rest[dur=2] layer')))

    def test_effective_meter(self):
        music   = MeiElement('music')
        body    = MeiElement('body')
        mdiv    = MeiElement('mdiv')
        score   = MeiElement('score')
        sctn    = MeiElement('section')
        scD1    = MeiElement('scoreDef')
        scD2    = MeiElement('scoreDef')
        stG1    = MeiElement('staffGrp')
        stG2    = MeiElement('staffGrp')
        stD1    = MeiElement('staffDef')
        stD2    = MeiElement('staffDef')

        m1      = MeiElement('measure')
        m2      = MeiElement('measure')
        l1      = MeiElement('layer')
        l2      = MeiElement('layer')
        s1      = MeiElement('staff')
        s2      = MeiElement('staff')

        mR1     = MeiElement('mRest')
        mR2     = MeiElement('mRest')

        scD1.addAttribute('meter.unit', '2')
        stD1.addAttribute('meter.count', '2')
        stD2.addAttribute('meter.count', '3')

        s1.addAttribute('n', '1')
        
        music.addChild(body)
        body.addChild(mdiv)
        mdiv.addChild(score)
        score.addChild(sctn)
        sctn.addChild(scD1)
        scD1.addChild(stG1)
        stG1.addChild(stD1)
        sctn.addChild(m1)
        m1.addChild(s1)
        s1.addChild(l1)
        l1.addChild(mR1)

        sctn.addChild(scD2)
        scD2.addChild(stG2)
        stG2.addChild(stD2)
        sctn.addChild(m2)
        m2.addChild(s2)
        s2.addChild(l2)
        l2.addChild(mR2)

        doc = MeiDocument()
        doc.setRootElement(music)

        meter1  = utilities.effective_meter(mR1)
        meter2  = utilities.effective_meter(mR2)

        self.assertEqual(meter1.count, '2')
        self.assertEqual(meter1.unit, '2')
        self.assertEqual(meter2.count, '3')
        self.assertEqual(meter2.unit, '2')

    def test_getattributeval(self):
        measure = MeiElement('measure')
        staff = MeiElement('staff')
        measure.addAttribute('n', '2')
        
        self.assertEqual(utilities.get_attribute_val(measure, 'n'), '2')
        self.assertEqual(utilities.get_attribute_val(staff, 'n', '1'), '1')

    def test_dur_in_semibreves_notes(self):
        music = MeiElement('music')
        body = MeiElement('body')
        mdiv = MeiElement('mdiv')
        score = MeiElement('score')
        section = MeiElement('section')

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
        nt8.addAttribute('dur', 'breve')
        nt9.addAttribute('dur', 'long')

        b = MeiElement('beam')
        nt10 = MeiElement('note')
        nt11 = MeiElement('note')
        nt10.addAttribute('dur', '4')
        nt11.addAttribute('dur', '4')
        b.addChild(nt10)
        b.addChild(nt11)

        c = MeiElement('chord')
        nt12 = MeiElement('note')
        nt13 = MeiElement('note')
        nt12.addAttribute('dur', '4')
        nt13.addAttribute('dur', '2')
        c.addChild(nt12)
        c.addChild(nt13)

        music.addChild(body)
        body.addChild(mdiv)
        mdiv.addChild(score)
        score.addChild(section)
        section.addChild(m1)
        m1.addChild(st1)
        st1.addChild(ly1)
        ly1.addChild(nt1)
        ly1.addChild(nt2)
        ly1.addChild(nt3)
        ly1.addChild(nt4)
        ly1.addChild(nt5)
        ly1.addChild(nt6)
        ly1.addChild(nt7)
        ly1.addChild(nt8)
        ly1.addChild(nt9)
        ly1.addChild(b)
        ly1.addChild(c)

        self.assertEqual(utilities.dur_in_semibreves(nt1), 1.0)
        self.assertEqual(utilities.dur_in_semibreves(nt2), 1.0/2.0)
        self.assertEqual(utilities.dur_in_semibreves(nt3), 1.0/4.0)
        self.assertEqual(utilities.dur_in_semibreves(nt4), 1.0/8.0)
        self.assertEqual(utilities.dur_in_semibreves(nt5), 1.0/16.0)
        self.assertEqual(utilities.dur_in_semibreves(nt6), 1.0/32.0)
        self.assertEqual(utilities.dur_in_semibreves(nt7), 1.0/64.0)
        self.assertEqual(utilities.dur_in_semibreves(nt8), 2.0)
        self.assertEqual(utilities.dur_in_semibreves(nt9), 4.0)
        self.assertEqual(utilities.dur_in_semibreves(b), 0.5)
        self.assertEqual(utilities.dur_in_semibreves(c), 0.5)

    def test_dur_in_semibreves_mRests(self):
        music = MeiElement('music')
        body = MeiElement('body')
        mdiv = MeiElement('mdiv')
        score = MeiElement('score')
        sctn = MeiElement('section')
        scD1 = MeiElement('scoreDef')
        scD2 = MeiElement('scoreDef')
        stG1 = MeiElement('staffGrp')
        stG2 = MeiElement('staffGrp')
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

        s1.addAttribute('n', '1')

        music.addChild(body)
        body.addChild(mdiv)
        mdiv.addChild(score)
        score.addChild(sctn)

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

        doc = MeiDocument()
        doc.setRootElement(music)

        self.assertEqual(doc.lookBack(body, 'music'), music)

        self.assertEqual(utilities.dur_in_semibreves(mR1), 1)
        self.assertEqual(utilities.dur_in_semibreves(mR2), 1.5)

    def test_getnextmeasure(self):
        section = MeiElement('section')
        m1 = MeiElement('measure')
        sb = MeiElement('sb')
        m2 = MeiElement('measure')
        
        section.addChild(m1)
        section.addChild(sb)
        section.addChild(m2)
        
        self.assertEqual(utilities.get_next_measure(m1), m2)
        self.assertEqual(utilities.get_next_measure(m2), None)

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
    parser = argparse.ArgumentParser(description='MEI-Massage a single file.')
    utilities.set_logging(parser)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
