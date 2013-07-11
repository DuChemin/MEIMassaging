# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
#	name = forms.CharField(max_length = 200)
	docfile = forms.FileField(
		label='Select a file',
		help_text='max. 42 megabytes'
	)

class MEIForm(forms.Form):
	docfile = forms.FileField()
	processType = forms.ChoiceField('variant', 'reconstruction')
