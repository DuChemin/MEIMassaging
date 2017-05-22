import sys
sys.path.insert(0, '..')

from arranger import arranger
from incipit import orig_clefs, number_of_incipit_measures
from incipit import obliterate_incipit, renumber_measures
from responsibility import responsibility
from longa import longa
from sources import sources_and_editors
from variants import variants
from emendations import emendations
from supplied import supplied_staves
from ignored import ignored
from cut_time import double_cut_time
from beams import eliminate_bad_beams
from remove_elements import cleanup_all_elements
from remove_attributes import cleanup_all_attributes
from invisible import make_invisible_space
from copyright import use_restrict
from ficta import mark_ficta

from constants import *
from utilities import source_name2NCName

import logging
# logging.basicConfig(filename=(MEDIA + 'transform.log'),level=logging.DEBUG)


class TransformData:
    # If you do not want to run the ficta function, use
    # `ficta=False` rather than `ficta=ANYCOLOR`.
    def __init__(self,
            alternates_list=[],
            arranger_to_editor=False,
            remove_incipit=True,
            editorial_resp='',
            replace_longa=False,
            color_for_variants=ANYCOLOR,
            color_for_emendations=ANYCOLOR,
            color_for_ficta=ANYCOLOR,
            double_cut_time=True,
            eliminate_bad_beams=True,
            make_invisible_space=True,
            copyright_text=None,
            cleanup=True,
        ):
        # The alternates_list field contains information about variants,
        # emendations and reconstructions. It is a list of 4-tuples.
        # A basic file with only four staves will look like this:
        #     [('1', VARIANT, '1', ''), ('2', VARIANT, '2', ''),
        #      ('3', VARIANT, '3', ''), ('4', VARIANT, '4', '')]
        # The first element represents the number of the derivative staff
        # under consideration. Other possible values for the middle element
        # are EMENDATION, RECONSTRUCTION and CONCORDANCE. The third element
        # represents the number of the parent staff. The tuple
        # ('5', RECONSTRUCTION, '2', '') can be read as
        # "staff 5 is a reconstruction of staff 2".
        # The last element represents source or responsibility.
        self.alternates_list = alternates_list
        self.arranger_to_editor = arranger_to_editor
        self.remove_incipit = remove_incipit
        self.replace_longa = replace_longa
        self.editorial_resp = editorial_resp
        self.color_for_variants = color_for_variants
        self.color_for_emendations = color_for_emendations
        self.color_for_ficta = color_for_ficta
        self.double_cut_time = double_cut_time
        self.eliminate_bad_beams = eliminate_bad_beams
        self.make_invisible_space = make_invisible_space
        self.copyright_text = copyright_text
        self.cleanup = cleanup


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
    logging.info('color_for_ficta: ' + str(data.color_for_ficta))
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
    if data.make_invisible_space:
        make_invisible_space(MEI_tree)
    if data.copyright_text:
        use_restrict(MEI_tree, data.copyright_text)
    ## The following not needed because they are handled by mei-filter.js
    # remove_annot_brackets(MEI_tree)
    # remove_metersig(MEI_tree)
    responsibility(MEI_tree, data.editorial_resp)

    # Only now should we do the tricky stuff.
    if data.color_for_ficta:
        # Add remove_color=False to leave the ficta note colored
        mark_ficta(MEI_tree, data.color_for_ficta, data.alternates_list)
    sources_and_editors(MEI_tree, data.alternates_list)
    variants(MEI_tree, data.alternates_list, data.color_for_variants)
    emendations(MEI_tree, data.alternates_list, data.color_for_emendations)
    supplied_staves(MEI_tree,
                    data.alternates_list,
                    [BLANK,
                     RECONSTRUCTION,
                     CONCORDANCE]
                    )

    ignored(MEI_tree, data.alternates_list)

    # Finally, clean up unwanted elements

    if data.cleanup:
        cleanup_all_elements(MEI_tree)
        cleanup_all_attributes(MEI_tree)

    # To do: remove ties from removed staves

    return MEI_doc
