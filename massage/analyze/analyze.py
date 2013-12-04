
import first_measure_empty
import editorial
# import orig_clefs_missing
import staves

from pymei import XmlImport

PATH = 'massage/massage/media/'

class AnalyzeData:
	def __init__(self,
			first_measure_empty,
			has_editor_element,
			has_arranger_element,
			editor_name,
			staff_list):
		self.first_measure_empty = first_measure_empty
		self.has_editor_element = has_editor_element
		self.has_arranger_element = has_arranger_element
		self.editor_name = editor_name
		self.staff_list = staff_list
		# self.orig_clefs_missing = orig_clefs_missing

def analyze(MEI_filename):
	MEI_doc = XmlImport.documentFromFile(MEI_filename)
	MEI_tree = MEI_doc.getRootElement()
	first_measure_empty_ = first_measure_empty.first_measure_empty(MEI_tree)
	has_editor_element_ = editorial.has_editor_element(MEI_tree)
	has_arranger_element_ = editorial.has_arranger_element(MEI_tree)
	editor_name_ = editorial.editor_name(MEI_tree)
	# orig_clefs_missing_ = orig_clefs_missing.orig_clefs_missing(MEI_tree)
	staff_list_ = staves.staff_list(MEI_tree)
	return AnalyzeData(first_measure_empty_,
			has_editor_element_,
			has_arranger_element_,
			editor_name_,
			staff_list_)

if __name__ == "__main__":
	pass

#                               _
#  _._ _..._ .-',     _.._(`))
# '-. `     '  /-._.-'    ',/
#    )         \            '.
#   / _    _    |             \
#  |  a    a    /              |
#  \   .-.                     ;  
#   '-('' ).-'       ,'       ;
#      '-;           |      .'
#         \           \    /
#         | 7  .__  _.-\   \
#         | |  |  ``/  /`  /
#        /,_|  |   /,_/   /
#           /,_/      '`-'
#
#      E A S T E R   P I G
