
from pymei import XmlImport
from staff_names import staff_names
from orig_clefs_missing import orig_clefs_missing

class AnalyzeData:
	def __init__(self, staff_names, orig_clefs_missing):
		self.staff_names = staff_names
		self.orig_clefs_missing = orig_clefs_missing

	def __repr__(self):
		r = ''
		r += 'Staff names:\n'
		for name in self.staff_names:
			r += ' * '
			r += name
			r += '\n'
		r += ('Original clefs ' + ('not ' if self.orig_clefs_missing else '') +
		      'missing')
		return r

def analyze(MEI_filename):
	MEI_doc = XmlImport.documentFromFile(MEI_filename)
	MEI_tree = MEI_doc.getRootElement()
	this_staff_names = staff_names(MEI_tree)
	this_orig_clefs_missing = orig_clefs_missing(MEI_tree)
	return AnalyzeData(this_staff_names, this_orig_clefs_missing)

if __name__ == "__main__":
	# For testing
	print(analyze('minimal.mei'))
