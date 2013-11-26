
from constants import *
# from pymei import MeiElement

def emendations(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the emendations,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	# emendation_list = [i for i in alternates_list
	# 		if i[1] == EMENDATION and i[0] != i[2]]
	# for measure in MEI_tree.getDescendantsByName('measure'):
	# 	add_all_apps_in_measure2(measure, variants_list)
	# 	remove_measure_var_staves(measure, variants_list)
	# delete_staff_def(MEI_tree, variants_list)

	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	for i in alternates_list:
		pass

