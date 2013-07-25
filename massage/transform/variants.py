
from constants import *
# from pymei import MeiElement

def variants(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	for i in alternates_list:
		pass
