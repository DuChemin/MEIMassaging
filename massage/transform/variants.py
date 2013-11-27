
from constants import *
from alt import local_alternatives
# from pymei import MeiElement

def variants(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	local_alternatives(MEI_tree, alternates_list, VARIANT)

