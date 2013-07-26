
from constants import *
from pymei import MeiElement

def reconstructions(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the reconstructions,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	all_staves = MEI_tree.getDescendantsByName('staff')
	# Find out which staves will need to be replaced by <app>.
	# Also collect list of ALL staves that will be kept;
	# should be just the top four, but doesn't hurt to check.
	all_keeper_staves_NUM = []
	staves_needing_app_NUM = []
	for i in alternates_list:
		if i[2] not in all_keeper_staves_NUM:
			all_keeper_staves_NUM.append(i[2])
		if i[2] not in staves_needing_app_NUM and i[1] == RECONSTRUCTION:
				staves_needing_app_NUM.append(i[2])
	# Now make corresponding lists that have the actual staff elements,
	# not just the numbers.
	staves_needing_app = []
	all_keeper_staves = []
	for staff in all_staves:
		if staff.getAttribute('n').getValue() in all_keeper_staves_NUM:
			all_keeper_staves.append(staff)
		if staff.getAttribute('n').getValue() in staves_needing_app_NUM:
			staves_needing_app.append(staff)

	# Go through list of keeper staves. If it's one that needs to be
	# turned into an <app> (should be blank), then do so.
	for staff in all_keeper_staves:
		parent_measure = staff.getParent()
		old_staff_number = staff.getAttribute('n').getValue()
		if staff in staves_needing_app:
			new_app = MeiElement('app')
			new_app.addAttribute('n', old_staff_number)
			new_app.addAttribute('type', RECONSTRUCTION)
			# Add <app> where <staff> was, and delete the latter
			parent_measure.removeChild(staff)
			parent_measure.addChild(new_app)
		# Otherwise, remove it and add it again, so that it will
		# be in its proper (numerical-order) place.
		else:
			parent_measure.removeChild(staff)
			parent_measure.addChild(staff)
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
							# Number <rdg> with old staff number
							new_rdg.addAttribute('n', i[0])
							# Add responsibility to new reading element
							new_rdg.addAttribute('resp', '#' + i[3])
							# Renumber staff with parent staff number,
							# which will be the same as the <app> number
							staff.addAttribute('n', i[2])
							app.addChild(new_rdg)
							new_rdg.addChild(staff)
							parent_measure.removeChild(staff)

	# Finally, adjust the <staffGrp> definition by removing definitions
	# for staves not in the list of keepers.
	all_staff_def = MEI_tree.getDescendantsByName('staffDef')
	for staff_def in all_staff_def:
		if staff_def.getAttribute('n').getValue() not in all_keeper_staves_NUM:
			staff_def.getParent().removeChild(staff_def)

# END

