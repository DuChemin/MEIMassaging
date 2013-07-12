
import analyze.staff_info
import analyze.orig_clefs_missing
# from pymei import XmlImport

class AnalyzeData:
	def __init__(self, staff_info, orig_clefs_missing):
		self.staff_info = staff_info
		self.orig_clefs_missing = orig_clefs_missing

def analyze(MEI_filename):
	MEI_doc = XmlImport.documentFromFile(MEI_filename)
	MEI_tree = MEI_doc.getRootElement()
	staff_info = staff_info.staff_info(MEI_doc)
	orig_clefs_missing = orig_clefs_missing.orig_clefs_missing(MEI_doc)
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
