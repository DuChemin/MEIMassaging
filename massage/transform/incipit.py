
from constants import *
# from pymei import MeiElement

def obliterate_incipit(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	first_measure = all_measures[0]
	first_measure.getParent().removeChild(first_measure)

def renumber_measures(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	for measure in all_measures:
		# Get measure number attribute
		attr_measure_number = measure.getAttribute('n')
		val_measure_number = attr_measure_number.getValue()
		# Reduce number by one
		attr_measure_number.setValue(val_measure_number - 1)
