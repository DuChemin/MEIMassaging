
from constants import *
from pymei import MeiElement

def reconstructions(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the reconstructions,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	all_staves = MEI_tree.getDescendantsByName('staff')
	# First, find out which staves will need to be replaced by <app>
	staves_needing_app = []
	for i in alternates_list:
		if i[2] not in staves_needing_app and i[1] == RECONSTRUCTION:
			i.append(i[2])
	# Go through, looking for original (blank) staves and replacing
	# them with <app> elements
	for k in staves_needing_app:
		for staff in all_staves:
			if staff.getAttribute('n').getValue() == k:
				new_app = MeiElement('app')
				new_app.addAttribute('n', k)
				# Add <app> where <staff> was, and delete the latter
				parent_measure = staff.getParent()
				parent_measure.addChild(new_app)
				parent_measure.removeChild(staff)
	# Go through one more time, this time looking for the reconstructed staves
	for i in alternates_list:
		if i[0] != i[2] and i[1] == RECONSTRUCTION:
			for staff in all_staves:
				# Find the new staff by number
				if staff.getAttribute('n').getValue() == i[0]:
					# Add it under its sibling <app>
					parent_measure = staff.getParent()
					sibling_apps = parent_measure.getChildrenByName('app')
					for app in sibling_apps:
						# If it's the right <app> element -- that is,
						# the number matches with the original staff
						# for this reconstruction
						if app.getAttribute('n').getValue() == i[2]:
							new_rdg = MeiElement('rdg')
							new_rdg.addAttribute('n', i[0])
							app.addChild(new_rdg)
							new_rdg.addChild(staff)
							parent_measure.removeChild(staff)
