import sys
sys.path.insert(0, '..')

from arranger import arranger
from incipit import obliterate_incipit, renumber_measures, orig_clefs, number_of_incipit_measures
from responsibility import responsibility
from longa import longa
from sources import sources_and_editors
from variants import variants
from emendations import emendations
from reconstructions import reconstructions
from ignored import ignored
from cut_time import double_cut_time
from beams import eliminate_bad_beams
from syllables import remove_empty_syllables
from annot import remove_annot_brackets
from metersig import remove_metersig

from constants import *
from utilities import source_name2NCName

import logging
# logging.basicConfig(filename=(MEDIA + 'transform.log'),level=logging.DEBUG)


class TransformData:
    def __init__(self,
            alternates_list=[],
            arranger_to_editor=False,
            remove_incipit=True,
            editorial_resp='',
            replace_longa=False,
            color_for_variants=ANYCOLOR,
            color_for_emendations=ANYCOLOR,
            double_cut_time=True,
            eliminate_bad_beams=True,
            remove_empty_syllables=True,
            remove_annot_brackets=True,
            remove_metersig=True,
        ):
        # The alternates_list field contains information about variants,
        # emendations and reconstructions. It is a list of 4-tuples.
        # A basic file with only four staves will look like this:
        #     [('1', VARIANT, '1', ''), ('2', VARIANT, '2', ''),
        #      ('3', VARIANT, '3', ''), ('4', VARIANT, '4', '')]
        # The first element represents the number of the derivative staff
        # under consideration. Other possible values for the middle element
        # are EMENDATION and RECONSTRUCTION. The third element represents
        # the number of the parent staff. The tuple ('5', RECONSTRUCTION, '2', '')
        # can be read as "staff 5 is a reconstruction of staff 2".
        # The last element represents source or responsibility.
        self.alternates_list = alternates_list
        self.arranger_to_editor = arranger_to_editor
        self.remove_incipit = remove_incipit
        self.replace_longa = replace_longa
        self.editorial_resp = editorial_resp
        self.color_for_variants = color_for_variants
        self.color_for_emendations = color_for_emendations
        self.double_cut_time = double_cut_time
        self.eliminate_bad_beams = eliminate_bad_beams
        self.remove_empty_syllables = remove_empty_syllables
        self.remove_annot_brackets = remove_annot_brackets
        self.remove_metersig = remove_metersig


def validate_ncnames(alternates_list):
    res_list = []
    for alternates_item in alternates_list:
        res_item = (alternates_item[0],
                    alternates_item[1],
                    alternates_item[2],
                    source_name2NCName(alternates_item[3])
                    )
        res_list.append(res_item)
    return res_list


def transform(MEI_doc, data=TransformData()):
    logging.info('alternates_list: ' + str(data.alternates_list))
    logging.info('arranger_to_editor: ' + str(data.arranger_to_editor))
    logging.info('remove_incipit: ' + str(data.remove_incipit))
    logging.info('replace_longa: ' + str(data.replace_longa))
    logging.info('editorial_resp: ' + str(data.editorial_resp))
    logging.info('color_for_variants: ' + str(data.color_for_variants))
    logging.info('color_for_emendations: ' + str(data.color_for_emendations))
    MEI_tree = MEI_doc.getRootElement()
    data.alternates_list = validate_ncnames(data.alternates_list)
    orig_clefs(MEI_tree, data.alternates_list)
    # Important : measure renumbering must be done after the
    # transcription clef info is compiled back into the main scoreDef
    if data.remove_incipit:
        number_of_measures_to_remove = number_of_incipit_measures(MEI_tree)
        logging.warning(str(number_of_measures_to_remove) +
                " measures will be removed from the start of the piece")
        obliterate_incipit(MEI_tree, number_of_measures_to_remove)
        renumber_measures(MEI_tree, number_of_measures_to_remove)
    if data.arranger_to_editor:
        arranger(MEI_tree)
    if data.replace_longa:
        longa(MEI_tree)
    if data.double_cut_time:
        double_cut_time(MEI_tree)
    if data.eliminate_bad_beams:
        eliminate_bad_beams(MEI_tree)
    if data.remove_empty_syllables:
        remove_empty_syllables(MEI_tree)
    if data.remove_annot_brackets:
        remove_annot_brackets(MEI_tree)
    if data.remove_metersig:
        remove_metersig(MEI_tree)
    responsibility(MEI_tree, data.editorial_resp)

    # Only now should we do the tricky stuff.
    sources_and_editors(MEI_tree, data.alternates_list)
    variants(MEI_tree, data.alternates_list, data.color_for_variants)
    emendations(MEI_tree, data.alternates_list, data.color_for_emendations)
    reconstructions(MEI_tree, data.alternates_list)
    ignored(MEI_tree, data.alternates_list)

    # To do: remove ties from removed staves

    return MEI_doc
