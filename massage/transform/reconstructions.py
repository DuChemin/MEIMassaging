
from constants import *
from pymei import MeiElement
from utilities import get_all_staves

def get_original_staves(MEI_tree, alternates_list):
	"""Returns a list of all staff objects of which other staff objects
	are marked as reconstructions; i.e. the ones whose staff information
	should be removed, though their place in the staff group will be held.
	"""
	# Get numbers of such staves
	original_staves_NUM = []
	for i in alternates_list:
		if i[2] not in original_staves_NUM and i[1] == RECONSTRUCTION:
			original_staves_NUM.append(i[2])
	# Now get list of actuall staff objects
	all_staves = get_all_staves(MEI_tree)
	original_staves = []
	for staff in all_staves:
		if staff.getAttribute('n').getValue() in original_staves_NUM:
			original_staves.append(staff)
	return original_staves

def get_recon_staves_NUM(MEI_tree, alternates_list):
	"""Get numbers of all reconstructed staevs."""
	recon_staves_NUM = []
	for i in alternates_list:
		if i[0] not in recon_staves_NUM and i[1] == RECONSTRUCTION:
			recon_staves_NUM.append(i[0])
	return recon_staves_NUM

def get_recon_staves(MEI_tree, alternates_list):
	"""Returns a list of all staff objects that are reconstructions of
	other staves, and should be moved inside the <app> of those staves.
	"""
	recon_staves_NUM = get_recon_staves_NUM(MEI_tree, alternates_list)
	# Now get list of actuall staff objects
	all_staves = get_all_staves(MEI_tree)
	recon_staves = []
	for staff in all_staves:
		if staff.getAttribute('n').getValue() in recon_staves_NUM:
			recon_staves.append(staff)
	return recon_staves

def make_orig_app(MEI_tree, original_staves):
	"""Based on the list of original staves, change their contents
	into empty <app> elements.
	"""
	all_staves = get_all_staves(MEI_tree)
	# Go through all staves to maintain original order
	for staff in all_staves:
		parent_measure = staff.getParent()
		old_staff_n = staff.getAttribute('n').getValue()
		# For original staves, which should be replaced with <app>:
		if staff in original_staves:
			new_app = MeiElement('app')
			new_app.addAttribute('n', old_staff_n)
			new_app.addAttribute('type', RECONSTRUCTION)
			# Add <app> where <staff> was, and delete the latter
			parent_measure.removeChild(staff)
			parent_measure.addChild(new_app)
		# Otherwise, remove it and add it again, so that it will
		# be in its proper (numerical-order) place.
		else:
			parent_measure.removeChild(staff)
			parent_measure.addChild(staff)

def move_recon_staves(recon_staves, al):
	"""Move reconstructed staves to their proper place within
	the <app> element created under the original staff.
	"""
	def orig(staff_n, alternates_list):
		"""Return the number of staff that the given staff
		is a reconstruction of.
		"""
		for i in alternates_list:
			if i[0] == staff_n:
				return i[2]

	def resp(staff_n, alternates_list):
		for i in alternates_list:
			if i[0] == staff_n:
				return i[3]

	for staff in recon_staves:
		staff_n = staff.getAttribute('n').getValue()
		parent_measure = staff.getParent()
		sibling_apps = parent_measure.getChildrenByName('app')
		for app in sibling_apps:
			# If it's the right <app> element -- that is,
			# the number matches with the original staff
			# for this reconstruction
			if orig(staff_n, al) == app.getAttribute('n').getValue():
				new_rdg = MeiElement('rdg')
				# Number <rdg> with old staff number
				new_rdg.addAttribute('n', staff_n)
				# Add responsibility to new reading element
				new_rdg.addAttribute('resp', '#' + resp(staff_n, al))
				# Renumber staff with parent staff number,
				# which will be the same as the <app> number
				staff.addAttribute('n', orig(staff_n, al))
				app.addChild(new_rdg)
				new_rdg.addChild(staff)
				parent_measure.removeChild(staff)

def adjust_staff_group(MEI_tree, recon_staves_NUM):
	"""Adjusts <staffGrp> definitions by removing definitions
	for reconstructed staves.
	"""
	all_staff_def = MEI_tree.getDescendantsByName('staffDef')
	for staff_def in all_staff_def:
		if staff_def.getAttribute('n').getValue() in recon_staves_NUM:
			staff_def.getParent().removeChild(staff_def)

def reconstructions(MEI_tree, alternates_list):
	original_staves = get_original_staves(MEI_tree, alternates_list)
	recon_staves_NUM = get_recon_staves_NUM(MEI_tree, alternates_list)
	recon_staves = get_recon_staves(MEI_tree, alternates_list)

	make_orig_app(MEI_tree, original_staves)
	move_recon_staves(recon_staves, alternates_list)
	adjust_staff_group(MEI_tree, recon_staves_NUM)
	

	

# END OF FILE

