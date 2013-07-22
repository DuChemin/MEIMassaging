import sys
sys.path.insert(0, '..')

from constants import *

def first_measure_empty(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	first_measure = all_measures[0]
	# Gets all the staves in the first measure
	first_staves = first_measure.getChildrenByName('staff')
	# If all of those are empty, return True;
	# if one is not empty, return False.
	for staff in first_staves:
		if staff.getChildren() != []:
			return False
	return True

if __name__ == "__main__":
	pass
