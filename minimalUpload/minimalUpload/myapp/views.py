# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from minimalUpload.myapp.models import Document
from minimalUpload.myapp.forms import DocumentForm

def list(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('minimalUpload.myapp.views.list'))
	else:
		form = DocumentForm() # A empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
		'myapp/list.html',
		{'documents': documents, 'form': form},
		context_instance=RequestContext(request)
	)

def process(request, a, b, c):
	html = "<html><body>haha no</body></html>"
	return HttpResponse(html)
