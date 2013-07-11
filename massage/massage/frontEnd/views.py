# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../../../analyze')

from analyze import analyze
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
	return render_to_response(
		'frontEnd/list.html',
		{'documents': documents, 'form': form},
		context_instance=RequestContext(request)
	)

def select(request):

	# if request.method == 'POST':
	# 	form = MEIForm(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		newdoc = Document(docfile = request.FILES['docfile'])
	# 		newdoc.save()
	# else:
	# 	form = MEIForm()

	documents = Document.objects.all()

	return render_to_response(
		'frontEnd/select.html',
		{'documents': documents},
		context_instance=RequestContext(request)
	)

def metadata(request):
	html = "<html><body>"
	if request.method == 'POST':
		html += "processing "

		processFile = request.POST.get('selection')
		html += processFile

	else:
		html = "<html><body>No file selected</body></html>"

	html += "</body></html>"



	return render_to_response(
		'frontEnd/metadata.html',
		{'document': processFile},
		context_instance=RequestContext(request)
		)
	# return HttpResponse(html)
