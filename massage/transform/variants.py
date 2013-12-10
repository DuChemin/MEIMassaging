
from constants import *
from alt import local_alternatives
from pymei import MeiElement
from utilities import chain_elems

def add_sourceDesc(MEI_tree, alternates_list):
	def add_source(sourceDesc, ali):
		print(sourceDesc)
		source = MeiElement('source')
		source.addAttribute('xml:id', ali[3])
		# relation = MeiElement('relation')
		# relation.addAtribute('target', )
		# relation.addAtribute('rel', 'hasAlternate')
		# source.addChild(relation)
		sourceDesc.addChild(source)
	
	sourceDesc = chain_elems(MEI_tree, ['meiHead', 'fileDesc', 'sourceDesc'])
	for item in alternates_list:
		if item[0] != item[2] and item[1] == VARIANT:
			add_source(sourceDesc, item)	

def variants(MEI_tree, alternates_list, color_we_want):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	add_sourceDesc(MEI_tree, alternates_list)
	local_alternatives(MEI_tree, alternates_list, color_we_want, VARIANT)

