import sys
sys.path.insert(0, '..')

from constants import *
from utilities import has_C_clef

def orig_clefs_missing(MEI_tree):
	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	for staffGrp in all_staffGrp:
		# Only check if not part of <orig> or <reg> to begin with
		if staffGrp.getParent().getName() not in [ORIG, REG]:
			if not has_C_clef(staffGrp):
				return True
	return False

if __name__ == "__main__":
	pass
