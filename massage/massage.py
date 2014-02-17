import sys
from analyze.analyze import analyze as make_analysis
from transform.transform import TransformData
from transform.transform import transform as transform_mei
from pymei import XmlImport, XmlExport

usage = "usage: python massage.py <mei-file>"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print usage
        exit()
    
    mei_file = sys.argv[1]
    analysis = make_analysis(mei_file)
    MEI_instructions = TransformData(
        arranger_to_editor=True,
        obliterate_incipit=analysis.first_measure_empty,
        replace_longa=True,
        editorial_resp=analysis.has_arranger_element,
        alternates_list=analysis.alternates_list)
    
    old_MEI_doc = XmlImport.documentFromFile(mei_file)
    new_MEI_doc = transform_mei(old_MEI_doc, MEI_instructions)
    XmlExport.meiDocumentToFile(new_MEI_doc, mei_file + ".msg.mei")
    

