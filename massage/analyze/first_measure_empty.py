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
		if has_children(staff) and not has_measure_rest(staff):
			return False
	return True

def has_children(MEI_tree):
	return MEI_tree.getChildren() != []

def has_measure_rest(MEI_tree):
	return MEI_tree.getDescendantsByName('mRest') != []

if __name__ == "__main__":
	pass
