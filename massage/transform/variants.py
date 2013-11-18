
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
	Exception: if BLACK is the "color we want", then
	return True for any *non-black* color.

	>>> color_matches('#0033ff', BLACK)
	True

	>>> color_matches(BLACK, BLACK)
	False

	>>> color_matches('#0033ff', '#0033ff')
	True

	>>> color_matches('#336699', '#0033ff')
	False
	"""
	if color_we_want == BLACK:
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

def semibreves_before(notelist, color_we_want=BLACK):
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

def duration_of_color(notelist, color_we_want=BLACK, begun_color=False):
	"""Gives the duration of the notes in the current layer
	with the given color, or any color if none is given.
	Only the first set of contiguous notes will be included.
	The color black (#000000) cannot be searched for; instead,
	the function will return the duration of the first non-black
	sequence of notes.

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
		return 0
	else:
		this_note = notelist[0]
		# Find duration of this note
		dur_attr = this_note.getAttribute('dur').getValue()
		this_duration = convert_to_semibreves(dur_attr)
		this_note_color = get_color(this_note)
		if not color_matches(this_note_color, color_we_want):
			if begun_color:
				return 0
			else:
				return duration_of_color(notelist[1:], color_we_want)
		else:
			return (this_duration +
					duration_of_color(notelist[1:], color_we_want, True))

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

def add_app_to_staff(staff, skip, duration):
	"""Modifies the <staff> element given by replacing its <layer>
	child element. The new layer will contain the same <note> elements
	as the original, but some of these notes will be nested inside an
	<app> element as the lemma; variants from other staves will also
	be added to this <app> as variant readings. The parameters skip
	and duration refer to the length in semibreves of the notes
	occurring before the <app> element is to begin, and the length
	in semibreves of the <app> element. We assume that there is
	only one layer in the staff given.
	
	Warning: relies on predictable ordering of getDescendantsByName().
	If this turns out not to be correct, this function must be rewritten
	to take a list of (skip, dur) tuples as a parameter and create all
	the <app> elements in one pass.
	"""
	old_layer = staff.getChildrenByName('layer')[0]
	notelist = old_layer.getDescendantsByName('note')
	new_layer = MeiElement('layer')
	app = MeiElement('app')
	lemma = MeiElement('lem')
	app.addChild(lemma)
	
	for note in notelist:
		dur_attr = note.getAttribute('dur').getValue()
		dur_of_next_note = convert_to_semibreves(dur_attr)
		# We haven't yet exhausted the skip; still adding notes
		# directly to the layer.
		if skip > 0 and dur_of_next_note <= skip:
			new_layer.addChild(note)
			skip -= dur_of_next_note
		# If the skip has been exhausted, begin the duration:
		elif duration > 0:
			# If this is the first time we're adding a note into the app,
			# this is the place to add the app element to the layer.
			if new_layer.getChildrenByName('app') == []:
				new_layer.addChild(app)
			# Otherwise, just read duration for this note.
			# Add the note to the <lemma>, within the <app>.
			else:
				duration -= dur_of_next_note
				lemma.addChild(note)
		# Skip and duration are both exhausted, and the rest
		# is just adding notes to the new layer.
		else:
			new_layer.addChild(note)
	# Finally, add new layer as a child of staff and remove the old one.
	staff.removeChild(old_layer)
	staff.addChild(new_layer)

def app_whole_measure(staff):
	"""Enclose the entire contents of a staff in a measure
	inside the <app> element. Will be done if variants overlap
	in illegal ways.
	"""
	old_layer = staff.getChildrenByName('layer')[0]
	notelist = old_layer.getDescendantsByName('note')
	new_layer = MeiElement('layer')
	app = MeiElement('app')
	lemma = MeiElement('lem')
	for note in notelist:
		lemma.addChild(note)
	app.addChild(lemma)
	new_layer.addChild(app)
	staff.removeChild(old_layer)
	staff.addChild(new_layer)

def legal_overlapping(staff, skipdurs):
	"""Takes a list of (skip, dur) tuples and returns a boolean value:
	True if the variants either line up or do not overlap,
	False if the variants overlap in an illegal way.
	"""
	def legal_with_lemma(staff, skip, dur):
		"""Returns whether the given skip and dur work
		with the given staff.
		"""
		old_layer = staff.getChildrenByName('layer')[0]
		new_layer = MeiElement('layer')
		notelist = old_layer.getDescendantsByName('note')
		for note in notelist:
			dur_attr = note.getAttribute('dur').getValue()
			dur_of_next_note = convert_to_semibreves(dur_attr)
			# During the skip
			if skip > 0:
				if dur_of_next_note <= skip:
					new_layer.addChild(note)
					skip -= dur_of_next_note
				else:
					return False
			else:
				if dur_of_next_note <= dur:
					dur -= dur_of_next_note
				else:
					return False
		return True

	def legal_with_each_other(skipA, durA, skipB, durB):
		"""Returns whether a skip, dur combination is legal with
		a single other skip, dur combination.
		"""
		# Case of non-overlapping
		if skipA + durA <= skipB or skipB + durB < skipA:
			return True
		# Case of complete lining-up
		elif skipA == skipB and durA == durB:
			return True
		# Case when one really has no dur (shouldn't happen?)
		elif durA == 0 or durB == 0:
			return True
		else:
			return False

	for sdA in skipdurs:
		if not legal_with_lemma(staff, sdA[0], sdA[1]):
			return False
		for sdB in skipdurs:
			if not legal_with_each_other(sdA[0], sdA[1], sdB[0], sdB[1]):
				return False
	return True

def get_staff_skipdurs(notelist):
		"""Get skip and duration information for a single notelist."""
		skipdurs = []
		for color in colors_in_notelist(notelist):
			skip = semibreves_before(notelist, color)
			dur = duration_of_color(notelist, color)
			skipdurs.append((skip, dur))
		return skipdurs

def add_all_apps_in_measure(measure, variants_list):
	def get_lemma_skipdurs(measure, lemma_n, vl):
		"""Get skip and duration information for each variant of each lemma."""
		if vl == []:
			return []
		else:
			if vl[0][2] == lemma_n:
				staff = get_staff(measure, vl[0][0])
				layer = staff.getChildrenByName('layer')[0]
				notelist = layer.getDescendantsByName('note')
				answer = get_staff_skipdurs(notelist)
			else:
				answer = []
			return answer + get_lemma_skipdurs(measure, lemma_n, vl[1:])

	# Determine if each variant group is legally lined up.
	# Get list of distinct lemma staff @n values:
	lemmas = []
	for v in variants_list:
		if v[2] not in lemmas:
			lemmas.append(v[2])
	for L in lemmas:
		lemma_skipdurs = get_lemma_skipdurs(measure, L, variants_list)
		if legal_overlapping(get_staff(measure, L), lemma_skipdurs):
			# remove duplicates with set()
			for sd in set(lemma_skipdurs):
				add_app_to_staff(get_staff(measure, L), sd[0], sd[1])
		else:
			app_whole_measure(get_staff(measure, L))

def add_measure_vars_to_app(measure, variants_list):
	"""Adds all variants in a measure to the lemma staff's <app>."""
	

def remove_measure_var_staves(measure, variants_list):
	"""Removes all extra variant staves, after their information
	has been added to the parent (lemma) staff.
	"""

def delete_staff_def(MEI_tree, variants_list):
	"""Deletes the staff definitions for variant staves."""

def variants(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	variants_list = [i for i in alternates_list
			if i[1] == VARIANT and i[0] != i[2]]
	for measure in MEI_tree.getDescendantsByName('measure'):
		add_all_apps_in_measure(measure, variants_list)
		add_measure_vars_to_app(measure, variants_list)
		remove_measure_var_staves(measure, variants_list)
	delete_staff_def(MEI_tree, variants_list)

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
