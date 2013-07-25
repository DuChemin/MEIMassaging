
import first_measure_empty
import orig_clefs_missing
import staff_names

from pymei import XmlImport

PATH = 'massage/massage/media/'

class AnalyzeData:
	def __init__(self,
	             first_measure_empty,
	             staff_names,
	             orig_clefs_missing):
		self.first_measure_empty = first_measure_empty
		self.staff_names = staff_names
		self.orig_clefs_missing = orig_clefs_missing

def analyze(MEI_filename):
	MEI_doc = XmlImport.documentFromFile(PATH + MEI_filename)
	MEI_tree = MEI_doc.getRootElement()
	first_measure_empty_ = first_measure_empty.first_measure_empty(MEI_tree)
	orig_clefs_missing_ = orig_clefs_missing.orig_clefs_missing(MEI_tree)
	staff_names_ = staff_names.staff_names(MEI_tree)
	return AnalyzeData(first_measure_empty_,
	                   staff_names_,
	                   orig_clefs_missing_)

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
