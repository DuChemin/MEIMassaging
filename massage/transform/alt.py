
from constants import *
from pymei import MeiElement
from utilities import get_descendants, Meter, effective_meter
import logging

class RichWrapperInsertError(Exception):
	def __init__(self, staff, skip, duration, ALT_TYPE, rich_wrapper):
		self.staff = staff
		self.skip = skip
		self.duration = duration
		self.ALT_TYPE = ALT_TYPE
		self.rich_wrapper = rich_wrapper

def get_notes(measure, staff_n):
	"""Return of all list of notes and rests in a given measure and staff."""
	for staff in measure:
		if staff.getAttribute('n').getValue():
			return staff.getDescendantsByName('note rest space')

def get_color(note):
		# If there is a note color attribute, save it;
		# default to black if the attribute doesn't exist
		# <space> cannot have color attribute, but we assume they are colored.
		if note.getName() == 'space':
			return ANYCOLOR
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

def dur_in_semibreves(elem):
	
	if elem.hasAttribute('dur'):
		dur_attr = elem.getAttribute('dur').getValue()
		if dur_attr == 'breve':
			return 2.0
		elif dur_attr == 'long':
			return 4.0
		else:
			return 1.0 / eval(dur_attr)
	elif elem.getName() == 'mRest':
		meter = effective_meter(elem)
		return meter.semibreves()
	else:
		return 0

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
	logging.debug('add_wrapper_to_staff(): ' + staff.getAttribute('n').value + ', s' + str(skip) + 'd' + str(duration))
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
	
	layer_notes = get_descendants(old_layer, 'note rest space mRest')
	if skip not in wrapperlist:
		logging.debug("There isn't any wrapper at position " + str(skip) + " yet. Creating wrapper.")
		rich_wrapper = MeiElement(rich_wrapper_name)
		rich_default_elem = MeiElement(rich_default_name)
		rich_wrapper.addChild(rich_default_elem)
		skip__ = skip
		logging.debug("Skipping notes in lemma that are before position " + str(skip) + ":")
		for note in layer_notes:
			dur_of_next_note = dur_in_semibreves(note)
			# We haven't yet exhausted the skip;
			if skip__ > 0 and dur_of_next_note <= skip__:
				skip__ -= dur_of_next_note
			# If the skip has been exhausted, begin the duration:
			elif duration > 0:
				if skip not in wrapperlist:
					logging.debug('adding new rich_wrapper at SKIP' + str(skip))
					wrappers_in_layer = old_layer.getChildrenByName(rich_wrapper_name)
					note.getParent().addChildBefore(note, rich_wrapper)
					wrapperlist[skip] = rich_wrapper
				note.getParent().removeChild(note)
				rich_default_elem.addChild(note)
				duration -= dur_of_next_note	
		if skip not in wrapperlist:
			raise RichWrapperInsertError(staff, skip, duration, ALT_TYPE, rich_wrapper)
	return wrapperlist[skip]


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
	old_layers = staff.getChildrenByName('layer')
	notelist = []
	if len(old_layers) > 0:
		old_layer = staff.getChildrenByName('layer')[0]
		notelist.extend(get_descendants(old_layer, 'note rest space'))
		staff.removeChild(old_layer)
	new_layer = MeiElement('layer')
	rich_wrapper = MeiElement(rich_wrapper_name)
	rich_default_elem = MeiElement(rich_default_name)
	for note in notelist:
		rich_default_elem.addChild(note)
	rich_wrapper.addChild(rich_default_elem)
	new_layer.addChild(rich_wrapper)
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
		logging.debug("legal_with_lemma(" + str(staff) + ", " + str(skip) + ", " + str(dur) +")")
		logging.debug('legal_with_lemma(): ' + staff.getAttribute('n').value + ', s' + str(skip) + 'd' + str(dur))
		old_layers = staff.getChildrenByName('layer')
		if len(old_layers) == 0:
			return False
		old_layer = old_layers[0]
		notelist = get_descendants(old_layer, 'note rest space mRest')
		for note in notelist:
			dur_of_next_note = dur_in_semibreves(note)
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
			logging.debug('Not legal with each-other: s' + str(skipA) + 'd' + str(durA) + ', and ' + 's' + str(skipB) + 'd' + str(durB))
			return False

	for sdA in skipdurs:
		if not legal_with_lemma(staff, sdA[1], sdA[2]):
			logging.debug('not legal with lemma')
			return False
		for sdB in skipdurs:
			if not legal_with_each_other(sdA[1], sdA[2], sdB[1], sdB[2]):
				logging.debug('not legal with each-other')
				return False
	return True
	
def get_colored_blocks(measure, lemma_n, vl, color_we_want): 
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
			notelist = get_descendants(layer, 'note rest space mRest')
			answer = [(staff, get_colored_blocks_from_notes(notelist, color_we_want))]
		else:
			answer = []
		return answer + get_colored_blocks(measure, lemma_n, vl[1:], color_we_want)
	
def get_colored_blocks_from_notes(notelist, color_we_want=ANYCOLOR): 
	"""Gather all colored blocks on a given staff
	Return a list of (color, skip, dur, notes)
	TODO: find colored blocks even if they are of the same color!
	"""
	skipdurs = []
	
	skip = 0
	dur = 0
	colored_notes = []
	for note in notelist:
		note_dur = dur_in_semibreves(note)
		note_color = get_color(note)
		if color_matches(note_color, color_we_want):
			curr_color = note_color
			dur += note_dur
			colored_notes.append(note)
		else:
			if dur>0:
				skipdurs.append((curr_color, skip, dur, colored_notes))
				skip = 0
				dur = 0
				colored_notes = []
			skip += note_dur
	if dur>0:
		skipdurs.append((curr_color, skip, dur, colored_notes))
	logging.debug(skipdurs)
	return skipdurs	

def add_rich_elems(measure, alternates_list, color_we_want, ALT_TYPE):
	"""Same as add_all_apps_in_measure, but using colored_blocks instead of (skip, dur) tuples
	"""
	def flatten_all_colored_blocks(list_of_list_of_color_blocks):
		FL = []
		for item in list_of_list_of_color_blocks:
			FL += item[1]
		return FL
	
	def source_of_variant(varstaff_n, variant_list):
		for v in variant_list:
			if varstaff_n == v[0]:
				return v[3]
	
	rich_item_name = 'rdg'
	rich_item_attr_name = 'source'
	if ALT_TYPE == EMENDATION:
		rich_item_name = 'corr'
		rich_item_attr_name = 'resp'
		
	# Determine if each variant group is legally lined up.
	# Get list of distinct lemma staff @n values:
	logging.debug('M' + str(measure.getAttribute('n').value))
	lemmas = []
	for v in alternates_list:
		if v[2] not in lemmas:
			lemmas.append(v[2])
	for L in lemmas:
		colored_blocks = get_colored_blocks(measure, L, alternates_list, color_we_want)
		staff = get_staff(measure, L)
		logging.debug('Lemma no. ' + L)
		logging.debug('All colored blocks for Lemma ' + str(L) + ': ' + str(colored_blocks))
		# TODO: merge sources where they coincide! -- HERE? or after having looked up source IDs? 
		#       Possibly do both at the same time...
		logging.debug("add_rich_elems {a}")
		flat_list_of_colored_blocks = flatten_all_colored_blocks(colored_blocks)
		logging.debug("add_rich_elems {b}")
		if legal_overlapping(staff, flat_list_of_colored_blocks):
			logging.debug("add_rich_elems {c.1}")
			wrapperlist = dict()
			RDGs_to_fill = []
			for cbs in colored_blocks:
				varstaff_n = cbs[0].getAttribute('n').getValue()
				# TODO: look up source ID from staffDef
				sourceID = '#' + source_of_variant(varstaff_n, alternates_list)
				for cb in cbs[1]:
					logging.debug("add_rich_elems() {A}: cb=" + str(cb))
					skip=cb[1]
					dur=cb[2]
					notelist=cb[3]
					try:
						rich_wrapper = add_wrapper_to_staff(staff, skip, dur, wrapperlist, ALT_TYPE)
						# add rdg elements with reference to notelist, but do not insert notelist yet.
						rdg = MeiElement(rich_item_name)
						rdg.addAttribute(rich_item_attr_name, sourceID)
						rich_wrapper.addChild(rdg)
						RDGs_to_fill.append((rdg, notelist))
					except RichWrapperInsertError as er:
						logging.warning("Coulnd't insert " + str(er.rich_wrapper) + " into measure:" + str(measure) + \
							"/staff:" + str(er.staff) + \
							'at skip=' + str(er.skip) + '; duration=' + str(er.duration))
			# fill in rdg elements 
			for rdgf in RDGs_to_fill:
				for note in rdgf[1]:
					logging.debug('adding child to rdg:')
					logging.debug(rdgf[0])
					rdgf[0].addChild(note)
		else:
			logging.debug("add_rich_elems {c.2}")
			rich_wrapper = wrap_whole_measure(staff, ALT_TYPE)
			# add rdg elements with reference to notelist, but do not insert notelist yet.
			for cbs in colored_blocks:
				varstaff_n = cbs[0].getAttribute('n').getValue()
				# TODO: look up source ID from staffDef
				sourceID = '#' + source_of_variant(varstaff_n, alternates_list)
				rdg = MeiElement(rich_item_name)
				rdg.addAttribute(rich_item_attr_name, sourceID)
				rich_wrapper.addChild(rdg)
				staves_of_measure = measure.getChildrenByName('staff')
				for staff in staves_of_measure:
					if staff.getAttribute('n').getValue() == varstaff_n:
						notelist = get_descendants(staff, 'note rest space')
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

def local_alternatives(MEI_tree, alternates_list, color_we_want, ALT_TYPE):
	"""Uses the list of alternate readings to find the variants,
	and reorganize the MEI file so that the alternate readings are
	grouped together with the lemma.
	"""
	logging.debug('Transforming ' + ALT_TYPE)
	# See transform.py for documentation for the alternates_list object.
	filtered_alternates_list = [i for i in alternates_list
			if i[1] == ALT_TYPE and i[0] != i[2]]
	for measure in MEI_tree.getDescendantsByName('measure'):
		logging.debug('measure: ' + measure.getAttribute('n').getValue())
		add_rich_elems(measure, filtered_alternates_list, color_we_want, ALT_TYPE)
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
