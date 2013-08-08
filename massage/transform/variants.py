
from constants import *
# from pymei import MeiElement

def get_notes(measure, staff_n):
	"""Return of all list of notes in a given measure and staff."""
	for staff in measure:
		if staff.getAttribute('n').getValue():
			return staff.getDescendantsByName('note')

def colors_in_measure(notelist):
	colors = []
	for note in notelist:
		if (note.hasAttribute('color') and
				note.getAttribute('color').getValue() not in colors):
			colors.append(note.getAttribute('color').getValue())
	return colors

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
	"""
	old_layer = staff.getChildrenByName('layer')[0]
	notelist = old_layer.getChildrenByName('note')
	new_layer = MeiElement('layer')
	
	# Add notes before the variant into the new layer
	while skip > 0 and notelist != []:
		dur_of_next_note = 1.0 / eval(
				notelist[0].getAttribute('dur').getValue())
		# Bad case where the variant doesn't line up with the lemma:
		# in this case, include the part of the lemma's note that
		# hangs outside its proper area.
		if dur_of_next_note > skip:
			# Add the difference to the duration of the <app>
			duration += dur_of_next_note - skip
			skip = 0
		# But in good cases, just add the next note
		else:
			new_layer.addChild(notelist[0])
			skip -= dur_of_next_note
			del notelist[0]

	# Now add the <app> to the layer; add the notes that belong in
	# the <app> to the lemma.
	app = MeiElement('app')
	lemma = MeiElement('lem')
	app.addChild(lemma)
	new_layer.addChild(app)
	while duration > 0 and notelist != []:
		dur_of_next_note = 1.0 / eval(
				notelist[0].getAttribute('dur').getValue())
		duration -= dur_of_next_note
		lemma.addChild(notelist[0])
		del notelist[0]

	# Add remaining notes, if any.
	while notelist != []:
		new_layer.addChild(notelist[0])
		del notelist[0]

	# Finally, add new layer as a child of staff and remove the old one.
	staff.removeChild(old_layer)
	staff.addChild(new_layer)

def incorporate_variant(MEI_tree, var_staff_n, orig_staff_n, color=BLACK):
	"""Given an MEI tree and two staff names, incorporate the variant
	into the original at each measure.
	"""
	measures = MEI_tree.getDescendantsByName('measure')
	for measure in measures:
		var_notelist = get_notes(measure, var_staff_n)
		skip = semibreves_before(var_notelist, color)
		duration = duration_of_color(var_notelist, color)

def variants(MEI_tree, alternates_list):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	# See transform.py for documentation for the alternates_list object.
	all_staffGrp = MEI_tree.getDescendantsByName('staffGrp')
	for i in alternates_list:
		if i[0] != i[2] and i[1] == VARIANT:
			pass
	# source, id

# END OF FILE

