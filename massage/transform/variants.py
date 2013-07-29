
from constants import *
# from pymei import MeiElement

def color_matches(this_note_color, color_we_want):
	if color_we_want == BLACK:
		return this_note_color != BLACK
	else:
		return this_note_color == color_we_want

def semibreves_before(notelist, color_we_want=BLACK):
	"""Gives the number of semibreves before the first occurrence
	either of the given color, or of any color if none is given.
	"""

	def get_color(note):
		# If there is a note color attribute, save it;
		# default to black if the attribute doesn't exist
		if not note.hasAttribute('color'):
			this_note_color = BLACK
		else:
			this_note_color = note.getAttribute('color').getValue()
		return this_note_color

	if notelist == []:
		return 0
	else:
		this_note = notelist[0]
		this_duration = 1.0 / eval(this_note.getAttribute('dur').getValue())
		this_note_color = get_color(this_note)
		if color_matches(this_note_color, color_we_want)
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
	"""
	if notelist == []:
		return 0
	else:
		this_note = notelist[0]
		this_duration = 1.0 / eval(this_note.getAttribute('dur').getValue())
		this_note_color = this_note.getAttribute('color').getValue()
		if not color_matches(this_note_color, color_we_want):
			if begun_color:
				return 0
			else:
				return duration_of_color(notelist[1:], color)
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

	def get_staff_by_number(measure, staff_n):
		for staff in measure.getChildrenByName('staff'):
			if staff.getAttribute('n').getValue() == staff_n:
				return staff
		# If it doesn't exist, we return a null...
		return None

	staff_n = staff.getAttribute('n')
	current_measure = staff.getParent()
	previous_measure = get_previous_measure(current_measure)
	# If we were at the beginning of the piece anyway, return default color
	if not previous_measure:
		return BLACK
	else:
		prev_measure_staff_n = get_staff_by_number(previous_measure)
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

def create_variant_app(lemma_layer, location, source=None, id=None):
	"""Creates an <app> element in the layer given, which will contain
	variants. The location parameter is a tuple of (skip, dur) --
	the number of semibreves before the first note of the variant,
	and the duration of all notes in the variant. The notes
	in the lemma corresponding to the skip and dur given will be
	moved to the <app> element.
	"""
	def calc_app_placement(notelist, skip, duration):
		if notelist == [] or duration == 0:
			return notelist
		else:
			pass
	pass

def variants(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	for i in alternates_list:
		pass
