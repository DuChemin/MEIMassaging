import sys
sys.path.insert(0, '..')

from constants import *
from re import split

def staff_list(MEI_tree):
	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	staff_list = []
	if len(all_staffGrp) < 1:
		print("Error: No staffGrp in file.")
	else:
		if len(all_staffGrp) > 1:
			print("Warning: more than one <staffGrp>; using first occurrence.")
		staffGrp = all_staffGrp[0]
		for staffDef in staffGrp.getDescendantsByName('staffDef'):
			staff_name = staffDef.getAttribute('label').getValue()
			staff_name_split = split('_', staff_name)

			staff_voice = staff_name_split[0]
			staff_type = VARIANT
			staff_source = ''
			if len(staff_name_split)>1:
				staff_type = staff_role(staff_name_split[1])
				if len(staff_name_split)>2:
					staff_source = staff_name_split[2]
			staff_list.append((staff_name, staff_voice, staff_type, staff_source))
	return staff_list

def staff_role(s):
	if 'recon' in s.lower():
		return RECONSTRUCTION
	elif 'emend' in s.lower() or 'amend' in s.lower():
		return EMENDATION
	elif 'variant' in s.lower():
		return VARIANT
	else:
		return 'UNKNOWN'

if __name__ == "__main__":
	pass
