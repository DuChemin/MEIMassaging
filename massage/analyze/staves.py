import sys
sys.path.insert(0, '..')

from constants import *

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
			staff_list.append((staff_name, staff_role(staff_name)))
	return staff_list

def staff_role(s):
	if 'recon' in s.lower():
		return RECONSTRUCTION
	elif 'emend' in s.lower() or 'amend' in s.lower():
		return EMENDATION
	else:
		return VARIANT

if __name__ == "__main__":
	pass
