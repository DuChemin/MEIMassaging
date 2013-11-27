
from constants import *
from pymei import MeiElement

def get_notes(measure, staff_n):
	"""Return of all list of notes in a given measure and staff."""
	for staff in measure:
		if staff.getAttribute('n').getValue():
			return staff.getDescendantsByName('note')

def get_color(note):
		# If there is a note color attribute, save it;
		# default to black if the attribute doesn't exist
		if not note.hasAttribute('color'):
			this_note_color = BLACK
		else:
			this_note_color = note.getAttribute('color').getValue()
		return this_note_color

def get_staff(measure, staff_n):
	for staff in measure.getDescendantsByName('staff'):
		if staff.getAttribute('n').getValue() == staff_n:
			return staff
	# If it doesn't exist, we return a null...
	return None

def colors_in_notelist(notelist):
	"""Returns a list of all non-black colors used in a given
	staff in a given measure (based on a list of notes).

	>>> note_black = MeiElement('note')
	>>> note_red = MeiElement('note')
	>>> note_red.addAttribute('color', RED)
	>>> note_blue = MeiElement('note')
	>>> note_blue.addAttribute('color', BLUE)
	>>> notelist = [note_black, note_red, note_blue]
	>>> colors_in_notelist(notelist)
	['#ff0000', '#0000ff']

	"""
	colors = []
	for note in notelist:
		color = get_color(note)
		if color not in colors and color != BLACK:
			colors.append(note.getAttribute('color').getValue())
	return colors

def color_matches(this_note_color, color_we_want):
	"""Does a given color match with the color we want?
	ANYCOLOR matches anything but BLACK

	>>> color_matches('#0033ff', '#0033ff')
	True

	>>> color_matches(BLACK, BLACK)
	True

	>>> color_matches('#336699', '#0033ff')
	False

	>>> color_matches(BLACK, ANYCOLOR)
	False

	>>> color_matches('#0033ff', ANYCOLOR)
	True

	"""
	if color_we_want == ANYCOLOR:
		return this_note_color != BLACK
	else:
		return this_note_color == color_we_want

def convert_to_semibreves(dur_attr):
	"""Converts an MEI @dur value to its equivalent
	in number of semibreves.
	"""
	if dur_attr == 'breve':
		return 2.0
	elif dur_attr == 'long':
		return 4.0
	else:
		return 1.0 / eval(dur_attr)

def semibreves_before(notelist, color_we_want=ANYCOLOR):
	"""Gives the number of semibreves before the first occurrence
	either of the given color, or of any color if none is given.

	>>> semibreve_black = MeiElement('note')
	>>> semibreve_black.addAttribute('dur', '1')
	>>> minim_black = MeiElement('note')
	>>> minim_black.addAttribute('dur', '2')
	>>> minim_red = MeiElement('note')
	>>> minim_red.addAttribute('dur', '2')
	>>> minim_red.addAttribute('color', RED)
	>>> breve_blue = MeiElement('note')
	>>> breve_blue.addAttribute('dur', 'breve')
	>>> breve_blue.addAttribute('color', BLUE)
	>>> notelist = [semibreve_black, minim_black, minim_red, breve_blue]
	>>> semibreves_before(notelist)
	1.5

	>>> semibreves_before(notelist, RED)
	1.5

	>>> semibreves_before(notelist, BLUE)
	2.0

	"""
	if notelist == []:
		return 0
	else:
		this_note = notelist[0]
		dur_attr = this_note.getAttribute('dur').getValue()
		this_duration = convert_to_semibreves(dur_attr)
		this_note_color = get_color(this_note)
		if color_matches(this_note_color, color_we_want):
			return 0
		else:
			return (this_duration +
					semibreves_before(notelist[1:], color_we_want))

def duration_of_color(notelist, color_we_want=ANYCOLOR, begun_color=False):
	"""Gives the duration of the notes in the current layer
	with the given color, or any color if none is given.
	Only the first set of contiguous notes will be included.

	>>> semibreve_black = MeiElement('note')
	>>> semibreve_black.addAttribute('dur', '1')
	>>> minim_black = MeiElement('note')
	>>> minim_black.addAttribute('dur', '2')
	>>> minim_red = MeiElement('note')
	>>> minim_red.addAttribute('dur', '2')
	>>> minim_red.addAttribute('color', RED)
	>>> breve_blue = MeiElement('note')
	>>> breve_blue.addAttribute('dur', 'breve')
	>>> breve_blue.addAttribute('color', BLUE)
	>>> notelist = [semibreve_black, minim_black, minim_red, breve_blue]
	>>> duration_of_color(notelist)
	0.5

	>>> duration_of_color(notelist, RED)
	0.5

	>>> duration_of_color(notelist, BLUE)
	2.0

	"""
	if notelist == []:
		return (0, [])
	else:
		this_note = notelist[0]
		# Find duration of this note
		dur_attr = this_note.getAttribute('dur').getValue()
		this_duration = convert_to_semibreves(dur_attr)
		this_note_color = get_color(this_note)
		if not color_matches(this_note_color, color_we_want):
			if begun_color:
				return (0, [])
			else:
				return duration_of_color(notelist[1:], color_we_want)
		else:
			sub_total = duration_of_color(notelist[1:], color_we_want, True)
			return (sub_total[0] + this_duration, sub_total[1] + [this_note])

def previous_measure_last_color(staff):
	"""Returns the color of the last note in the previous measure,
	in the same staff as that given.
	"""
	def get_previous_measure(current_measure):
		current_measure_n = current_measure.getAttribute('n').getValue()
		previous_measure_n = str(eval(current_measure_n) - 1)
		measure_parent = current_measure.getParent()
		for measure in measure_parent.getChildrenByName('measure'):
			if measure.getAttribute('n').getValue() == previous_measure_n:
				return measure
		# Otherwise, we had the first measure already...
		return None

	staff_n = staff.getAttribute('n')
	current_measure = staff.getParent()
	previous_measure = get_previous_measure(current_measure)
	# If we were at the beginning of the piece anyway, return default color
	if not previous_measure:
		return BLACK
	else:
		prev_measure_staff_n = get_staff(previous_measure)
		# Case which shouldn't happen: staff doesn't exist in previous measure
		if not prev_measure_staff_n:
			return BLACK

	prev_measure_notes = staff.getChildrenByName('note')
	# No notes in measure? Return default
	if prev_measure_notes == []:
		return BLACK
	# Also return default if no color attr to last note of measure
	elif not notes[-1].hasAttribute('color'):
		return BLACK
	else:
		return last_note.getAttribute('color').getValue()

def add_wrapper_to_staff(staff, skip, duration, wrapperlist, ALT_TYPE):
	# print('add_wrapper_to_staff(): ' + staff.getAttribute('n').value + ', s' + str(skip) + 'd' + str(duration))
	"""
	When ALT_TYPE == VARIANTS the method modifies the <staff> element 
	by wrapping the specified section of notes into an <app><lem/></app> 
	construct. The location of the <app> element is specified by the skip paramter, 
	and the length of the <app> element is defined by the dur parameter. 
	The parameters skip and duration refer to the length in semibreves 
	of the notes occurring before the <app> element is to begin, and the length
	in semibreves of the <app> element. We assume that there is
	only one layer in the staff given.
	
	The wrapperlist paramter is an in/out parameter. The created <app> object 
	is stored in wrapperlist. The wrapperlist paramter is a dictionary, and it is 
	indexed by the location of the app elements within the measure. There 
	can only be one <app> element at a given location. If there's already 
	an <app> element defined at the given location, the method returns 
	without making any modification to the staff.
	
	When ALT_TYPE == EMENDATIONS the method does exactly the same but uses
	the <choice><sic/></choice> construct instead of the critical apparatus
	elements.
		
	in-out parameters: staff, wrapperlist
	in paramteres: skip, duration
	
	Warning: relies on predictable ordering of getDescendantsByName().
	If this turns out not to be correct, this function must be rewritten
	to take a list of (skip, dur) tuples as a parameter and create all
	the <app> elements in one pass.
	"""
	rich_wrapper_name = 'app'	
	rich_default_name = 'lem'
	if ALT_TYPE == EMENDATION:
		rich_wrapper_name = 'choice'	
		rich_default_name = 'sic'

	old_layer = staff.getChildrenByName('layer')[0]	
	layer_notes = old_layer.getDescendantsByName('note')
	if skip not in wrapperlist:
		rich_wrapper = MeiElement(rich_wrapper_name)
		rich_default_elem = MeiElement(rich_default_name)
		rich_wrapper.addChild(rich_default_elem)
		skip__ = skip
		for note in layer_notes:
			dur_attr = note.getAttribute('dur').getValue()
			dur_of_next_note = convert_to_semibreves(dur_attr)
			# We haven't yet exhausted the skip;
			if skip__ > 0 and dur_of_next_note <= skip__:
				skip__ -= dur_of_next_note
			# If the skip has been exhausted, begin the duration:
			elif duration > 0:
				if skip not in wrapperlist:
					# print('adding new rich_wrapper at SKIP' + str(skip))
					wrappers_in_layer = old_layer.getChildrenByName(rich_wrapper_name)
					note.getParent().addChildBefore(note, rich_wrapper)
					wrapperlist[skip] = rich_wrapper
				note.getParent().removeChild(note)
				rich_default_elem.addChild(note)
				duration -= dur_of_next_note	

def wrap_whole_measure(staff, ALT_TYPE):
	"""Enclose the entire contents of a staff in a measure
	inside the <app> element. Will be done if variants overlap
	in illegal ways.
	"""
	rich_wrapper_name = 'app'	
	rich_default_name = 'lem'
	if ALT_TYPE == EMENDATION:
		rich_wrapper_name = 'choice'	
		rich_default_name = 'sic'
	old_layer = staff.getChildrenByName('layer')[0]
	notelist = old_layer.getDescendantsByName('note')
	new_layer = MeiElement('layer')
	rich_wrapper = MeiElement(rich_wrapper_name)
	rich_default_elem = MeiElement(rich_default_name)
	for note in notelist:
		rich_default_elem.addChild(note)
	rich_wrapper.addChild(rich_default_elem)
	new_layer.addChild(rich_wrapper)
	staff.removeChild(old_layer)
	staff.addChild(new_layer)
	return rich_wrapper

def legal_overlapping(staff, skipdurs):
	"""Takes a list of (skip, dur) tuples and returns a boolean value:
	True if the variants either line up or do not overlap,
	False if the variants overlap in an illegal way.
	"""
	def legal_with_lemma(staff, skip, dur):
		"""Returns whether the given skip and dur work
		with the given staff.
		"""
		# print('legal_with_lemma(): ' + staff.getAttribute('n').value + ', s' + str(skip) + 'd' + str(dur))
		old_layer = staff.getChildrenByName('layer')[0]
		notelist = old_layer.getDescendantsByName('note')
		for note in notelist:
			dur_attr = note.getAttribute('dur').getValue()
			dur_of_next_note = convert_to_semibreves(dur_attr)
			# During the skip
			if skip > 0:
				if dur_of_next_note <= skip:
					skip -= dur_of_next_note
				else:
					return False
			else:
				if dur_of_next_note <= dur:
					dur -= dur_of_next_note
				else:
					if dur > 0:
						return False
		return True

	def legal_with_each_other(skipA, durA, skipB, durB):
		"""Returns whether a skip, dur combination is legal with
		a single other skip, dur combination.
		"""
		# Case of non-overlapping
		if skipA + durA <= skipB or skipB + durB <= skipA:
			return True
		# Case of complete lining-up
		elif skipA == skipB and durA == durB:
			return True
		# Case when one really has no dur (shouldn't happen?)
		elif durA == 0 or durB == 0:
			return True
		else:
			# print('Not legal with each-other: s' + str(skipA) + 'd' + str(durA) + ', and ' + 's' + str(skipB) + 'd' + str(durB))
			return False

	for sdA in skipdurs:
		if not legal_with_lemma(staff, sdA[1], sdA[2]):
			# print('not legal with lemma')
			return False
		for sdB in skipdurs:
			if not legal_with_each_other(sdA[1], sdA[2], sdB[1], sdB[2]):
				# print('not legal with each-other')
				return False
	return True
	
def get_colored_blocks(measure, lemma_n, vl): 
	"""Gather all colored blocks from all variant staves in the given 
	measure and a given lemma staff
	Return a list of (staff, list of (color, skip, dur, notes))
	"""
	if vl == []:
		return []
	else:
		if vl[0][2] == lemma_n:
			staff = get_staff(measure, vl[0][0])
			layer = staff.getChildrenByName('layer')[0]
			notelist = layer.getDescendantsByName('note')
			answer = [(staff, get_colored_blocks_from_notes(notelist))]
		else:
			answer = []
		return answer + get_colored_blocks(measure, lemma_n, vl[1:])
	
def get_colored_blocks_from_notes(notelist): 
	"""Gather all colored blocks on a given staff
	Return a list of (color, skip, dur, notes)
	TODO: find colored blocks even if they are of the same color!
	"""
	# return [(BLACK, 0, 0, [])]
	skipdurs = []
	for color in colors_in_notelist(notelist):
		skip = semibreves_before(notelist, color)
		dur_and_notes = duration_of_color(notelist, color)
		dur = dur_and_notes[0]
		notelist = dur_and_notes[1]
		skipdurs.append((color, skip, dur, notelist))
	return skipdurs
	
def add_rich_elems(measure, alternates_list, ALT_TYPE):
	"""Same as add_all_apps_in_measure, but using colored_blocks instead of (skip, dur) tuples
	"""
	def flatten_all_colored_blocks(list_of_list_of_color_blocks):
		FL = []
		for item in list_of_list_of_color_blocks:
			FL += item[1]
		return FL
	
	rich_item_name = 'rdg'
	rich_item_attr_name = 'source'
	if ALT_TYPE == EMENDATION:
		rich_item_name = 'corr'
		rich_item_attr_name = 'resp'
		
	# Determine if each variant group is legally lined up.
	# Get list of distinct lemma staff @n values:
	# print('M' + str(measure.getAttribute('n').value))
	lemmas = []
	for v in alternates_list:
		if v[2] not in lemmas:
			lemmas.append(v[2])
	for L in lemmas:
		colored_blocks = get_colored_blocks(measure, L, alternates_list)
		staff = get_staff(measure, L)
		# print('Lemma no. ' + L)
		# print('All colored blocks for Lemma ' + str(L) + ': ' + str(colored_blocks))
		# TODO: merge sources where they coincide! -- HERE? or after having looked up source IDs? 
		#       Possibly do both at the same time...
		flat_list_of_colored_blocks = flatten_all_colored_blocks(colored_blocks)
		if legal_overlapping(staff, flat_list_of_colored_blocks):
			wrapperlist = dict()
			RDGs_to_fill = []
			for cbs in colored_blocks:
				varstaff_n = cbs[0].getAttribute('n').getValue()
				# TODO: look up source ID from staffDef
				sourceID = '#source_' + varstaff_n
				for cb in cbs[1]:
					# print("add_rich_elems() {A}: cb=" + str(cb))
					skip=cb[1]
					dur=cb[2]
					notelist=cb[3]
					add_wrapper_to_staff(staff, skip, dur, wrapperlist, ALT_TYPE)
					rich_wrapper = wrapperlist[skip]
					# add rdg elements with reference to notelist, but do not insert notelist yet.
					rdg = MeiElement(rich_item_name)
					rdg.addAttribute(rich_item_attr_name, sourceID)
					rich_wrapper.addChild(rdg)
					RDGs_to_fill.append((rdg, notelist))
			# fill in rdg elements 
			for rdgf in RDGs_to_fill:
				for note in rdgf[1]:
					# print('adding child to rdg:')
					# print(rdgf[0])
					rdgf[0].addChild(note)
		else:
			rich_wrapper = wrap_whole_measure(staff, ALT_TYPE)
			# add rdg elements with reference to notelist, but do not insert notelist yet.
			for cbs in colored_blocks:
				varstaff_n = cbs[0].getAttribute('n').getValue()
				# TODO: look up source ID from staffDef
				sourceID = '#source_' + varstaff_n
				rdg = MeiElement(rich_item_name)
				rdg.addAttribute(rich_item_attr_name, sourceID)
				rich_wrapper.addChild(rdg)
				staves_of_measure = measure.getChildrenByName('staff')
				for staff in staves_of_measure:
					if staff.getAttribute('n').getValue() == varstaff_n:
						notelist = staff.getDescendantsByName('note')
						for note in notelist:
							rdg.addChild(note)

def merge_identical_colored_blocks(all_colored_blocks):
	"""
	Reduce the number of distinct colored blocks by merge together identical blocks.
	As a result, a new (list of (varstaff, (list of (color, skip, dur, notelist))) is created. In the new set of
	colored blocks the following is true:
	  - if A and B two colored blocks AND A.skip==B.skip AND A.color==B.color THEN A.notelist != B.notelist
	"""
	# list of (varstaff, colored_blocks_by_skip) where colored_blocks_by_skip[skip][color]

def remove_measure_staves(measure, alternate_list):
	"""Removes all extra staves listed in alternate_list;
	"""
	staff_list = measure.getDescendantsByName('staff')
	for list_item in alternate_list:
		for staff in staff_list:
			if staff.hasAttribute('n') and staff.getAttribute('n').value == list_item[0]:
				staff.parent.removeChild(staff)

def delete_staff_def(MEI_tree, variants_list):
	"""Deletes the staff definitions for variant staves."""
	staffDefs = MEI_tree.getDescendantsByName('staffDef')
	for variants_list_item in variants_list:
		for staffDef in staffDefs:
			if staffDef.hasAttribute('n') and staffDef.getAttribute('n').value == variants_list_item[0]:
				staffDef.parent.removeChild(staffDef)

def local_alternatives(MEI_tree, alternates_list, ALT_TYPE):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# print('Transforming ' + ALT_TYPE)
	# See transform.py for documentation for the alternates_list object.
	filtered_alternates_list = [i for i in alternates_list
			if i[1] == ALT_TYPE and i[0] != i[2]]
	for measure in MEI_tree.getDescendantsByName('measure'):
		add_rich_elems(measure, filtered_alternates_list, ALT_TYPE)
		remove_measure_staves(measure, filtered_alternates_list)
	delete_staff_def(MEI_tree, filtered_alternates_list)
	
"""
To add in future:
 * add source information
 * add id information to <app> elements: this way
   variants that cross barlines can be kept together
 * put variants that are identical in multiple sources
   into the same <rdg> element
 * preserve brackets, ties and similar annotations
"""

# END OF FILE
