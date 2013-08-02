# -*- coding: utf-8 -*-
import sys

from analyze.analyze import analyze as make_analysis
from transform.transform import TransformData
from transform.transform import write_transformation
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from massage.frontEnd.models import Document
from massage.frontEnd.forms import DocumentForm

# from constants import *

def list(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(
					reverse('massage.frontEnd.views.select'))
	else:
		form = DocumentForm() # A empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render_to_response('frontEnd/list.html',
	                          {'documents': documents, 'form': form},
		context_instance=RequestContext(request)
	)

def select(request):
	documents = Document.objects.all()

	return render_to_response('frontEnd/select.html',
	                          {'documents': documents},
	                          context_instance=RequestContext(request)
	                         )

def selectTransform(request):
	documents = Document.objects.all()
	if request.method == 'POST':
		MEI_filename = request.POST.get('MEI_filename')
		arranger_to_editor = request.POST.get('arranger_to_editor')
		obliterate_incipit = request.POST.get('obliterate_incipit')
		replace_longa = request.POST.get('replace_longa')
		editorial_resp = request.POST.get('editorial_resp')

		alternates_list = []
		# staves = request.POST.get('staves')

		# To calculate number of staves
		sn = 0
		while request.POST.get('kindOfReading' + str(sn + 1)):
			sn += 1

		for j in range(1, sn + 1): # 1-indexed
			kind_of_reading = request.POST.get('kindOfReading' + str(j))
			reading_of = request.POST.get('readingOf' + str(j))
			source = request.POST.get('source' + str(j))
			this_staff_alternates = (str(j), str(kind_of_reading),
					str(reading_of), str(source))
			alternates_list.append(this_staff_alternates)

		# orig_clefs = []
		# for j in range(1, sn + 1): # 1-indexed
		# 	this_staff_orig_clef = request.POST.get('clef' + str(j))
		# 	orig_clefs.append(str(this_staff_orig_clef))

		MEI_instructions = TransformData(
				arranger_to_editor=arranger_to_editor,
				obliterate_incipit=obliterate_incipit,
				replace_longa=replace_longa,
				editorial_resp=editorial_resp,
				alternates_list=alternates_list)
		write_transformation(str(MEI_filename), MEI_instructions)

	return render_to_response('frontEnd/select.html',
	                          {'documents': documents},
	                          context_instance=RequestContext(request)
	                         )

def metadata(request):
	html = "<html><body>"
	if request.method == 'POST':
		MEI_filename = request.POST.get('selection')
		# str() converts from unicode to str
		analysis = make_analysis(str(MEI_filename))
		# "variant" or "reconstruction"
		processType = request.POST.get('processType')
	else:
		html = "<html><body>No file selected</body></html>"
		return HttpResponse(html)

	return render_to_response('frontEnd/metadata.html',
			{'MEI_filename': MEI_filename,
					'first_measure_empty': analysis.first_measure_empty,
					'has_editor_element': analysis.has_editor_element,
					'has_arranger_element': analysis.has_arranger_element,
					'editor_name': analysis.editor_name,
					'staff_list': analysis.staff_list
			},
			context_instance=RequestContext(request))
