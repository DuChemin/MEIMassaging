import editorial
import staves

from pymei import documentFromFile

PATH = 'massage/massage/media/'


class AnalyzeData:
    def __init__(self,
                 has_editor_element,
                 has_arranger_element,
                 editor_name,
                 staff_list,
                 alternates_list):
        self.has_editor_element = has_editor_element
        self.has_arranger_element = has_arranger_element
        self.editor_name = editor_name
        self.staff_list = staff_list
        self.alternates_list = alternates_list


def analyze(MEI_filename):
    res = documentFromFile(MEI_filename)
    MEI_doc = res.getMeiDocument()
    MEI_tree = MEI_doc.getRootElement()
    has_editor_element_ = editorial.has_editor_element(MEI_tree)
    has_arranger_element_ = editorial.has_arranger_element(MEI_tree)
    editor_name_ = editorial.editor_name(MEI_tree)
    staff_list_ = staves.staff_list(MEI_tree)
    alternates_list_ = staves.alternates_list(staff_list_)
    return AnalyzeData(has_editor_element_,
                       has_arranger_element_,
                       editor_name_,
                       staff_list_,
                       alternates_list_,
                       )
