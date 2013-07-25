
from constants import *
# from pymei import MeiElement

def obliterate_incipit(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	for measure in all_measures:
		if measure.getAttribute('n').getValue() == '1':
			measure.getParent().removeChild(measure)

def renumber_measures(MEI_tree):
	all_measures = MEI_tree.getDescendantsByName('measure')
	for measure in all_measures:
		# Get measure number attribute
		attr_measure_number = measure.getAttribute('n')
		val_measure_number = attr_measure_number.getValue()
		# Reduce number by one
		attr_measure_number.setValue(val_measure_number - 1)
