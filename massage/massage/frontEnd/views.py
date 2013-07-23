# -*- coding: utf-8 -*-
import sys

from analyze.analyze import analyze as make_analysis
from transform.transform import TransformData
from transform.transform import transform as make_transformation
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from massage.frontEnd.models import Document
from massage.frontEnd.forms import DocumentForm

def list(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('massage.frontEnd.views.select'))
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
		MEI_filename = request.POST.get('filename')
		arranger_to_editor = request.POST.get('arranger_to_editor')
		obliterate_incipit = request.POST.get('')
		orig_clefs = request.POST.get('')
		replace_longa = request.POST.get('')
		MEI_instructions = TransformData()
		make_transformation(MEI_filename, MEI_instructions)

	return render_to_response('frontEnd/select.html',
	                          {'documents': documents},
	                          context_instance=RequestContext(request)
	                         )

def metadata(request):
	html = "<html><body>"
	if request.method == 'POST':
		MEI_filename = request.POST.get('selection')
		analysis = make_analysis(str(MEI_filename))
		# "variant" or "reconstruction"
		processType = request.POST.get('processType')
	else:
		html = "<html><body>No file selected</body></html>"
		return HttpResponse(html)

	return render_to_response('frontEnd/metadata.html',
	                          {'document': MEI_filename,
	                           'first_measure_empty': analysis.first_measure_empty,
	                           'staves': analysis.staff_names
	                          },
	                           context_instance=RequestContext(request)
	                         )
