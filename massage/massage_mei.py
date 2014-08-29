import argparse
import logging
from analyze.analyze import analyze as make_analysis
from transform.transform import TransformData
from transform.transform import transform as transform_mei
from pymei import XmlImport, XmlExport
from utilities import set_logging


def massage_mei(in_file, out_file):
    try:
        analysis = make_analysis(in_file)
        MEI_instructions = TransformData(
            arranger_to_editor=True,
            remove_incipit=True,
            replace_longa=True,
            editorial_resp=analysis.has_arranger_element,
            alternates_list=analysis.alternates_list)
        old_MEI_doc = XmlImport.documentFromFile(in_file)
        new_MEI_doc = transform_mei(old_MEI_doc, MEI_instructions)
        XmlExport.meiDocumentToFile(new_MEI_doc, out_file)
    except Exception as ex:
        logging.critical(ex)
        logging.critical("Error during massaging " + in_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MEI-Massage a single file.')
    parser.add_argument('in_file')
    parser.add_argument('--out', dest='out_file')
    set_logging(parser)
    args = parser.parse_args()
    if not args.out_file:
        if '-orig' in args.in_file:
            args.out_file = args.in_file.replace('-orig', '')
        else:
            args.out_file = args.in_file + '_msg.mei'
    logging.info("Massage file: " + args.in_file)
    massage_mei(args.in_file, args.out_file)
    logging.info("DONE.")
