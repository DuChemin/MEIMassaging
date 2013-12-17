
from constants import *
from alt import local_alternatives
from pymei import MeiElement
from utilities import chain_elems

def variants(MEI_tree, alternates_list, color_we_want):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	local_alternatives(MEI_tree, alternates_list, color_we_want, VARIANT)

