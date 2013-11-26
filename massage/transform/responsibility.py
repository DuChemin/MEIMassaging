
from pymei import MeiElement

def responsibility(MEI_tree, resp):
	"""Adds @func and @resp attributes to editorial accidentals."""
	all_supplied = MEI_tree.getDescendantsByName('supplied')
	for supplied in all_supplied:
		supplied.addAttribute('reason', 'edit')
		if resp:
			supplied.addAttribute('resp', resp)
