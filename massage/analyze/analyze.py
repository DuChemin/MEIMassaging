
from first_measure_empty import first_measure_empty
from orig_clefs_missing import orig_clefs_missing
from staff_info import staff_info

from pymei import XmlImport

class AnalyzeData:
	def __init__(self,
	             first_measure_empty,
	             staff_info,
	             orig_clefs_missing):
		self.first_measure_empty = first_measure_empty
		self.staff_info = staff_info
		self.orig_clefs_missing = orig_clefs_missing

def analyze(MEI_filename):
	MEI_doc = XmlImport.documentFromFile(MEI_filename)
	MEI_tree = MEI_doc.getRootElement()
	first_measure_empty = first_measure_empty(MEI_doc)
	orig_clefs_missing = orig_clefs_missing(MEI_doc)
	staff_info = staff_info(MEI_doc)
	return AnalyzeData(staff_info, orig_clefs_missing)

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
