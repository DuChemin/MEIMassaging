def remove_empty_syllables(MEI_tree):
    """Removes all syllables with no text inside."""

    all_verses = MEI_tree.getDescendantsByName('verse')
    for verse in all_verses:
        syllables_in_verse = verse.getDescendantsByName('syl')
        for syl in syllables_in_verse:
            # Delete the syllable if it has no text inside
            if not syl.getValue():
                verse.removeChild(syl)
