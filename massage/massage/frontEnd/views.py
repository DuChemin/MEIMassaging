# -*- coding: utf-8 -*-
from analyze.analyze import analyze as make_analysis
from transform.transform import TransformData
from transform.transform import transform as transform_mei
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage

from massage.frontEnd.models import Document
from massage.frontEnd.forms import DocumentForm
# from pymei import XmlImport, XmlExport
from pymei import documentFromFile, documentToFile


def list(request):
    def process(request):
        def write_transformation(file_path, data=TransformData()):
            old_res = documentFromFile(file_path)
            old_MEI_doc = old_res.getMeiDocument()

            new_MEI_doc = transform_mei(old_MEI_doc, data)
            status = documentToFile(new_MEI_doc, file_path)

        if request.method == 'POST':
            MEI_filename = request.POST.get('MEI_filename')
            arranger_to_editor = request.POST.get('arranger_to_editor')
            obliterate_incipit = request.POST.get('obliterate_incipit')
            replace_longa = request.POST.get('replace_longa')
            editorial_resp = str(request.POST.get('editorial_resp'))
            color_for_ficta = str(request.POST.get('color_for_ficta'))
            alternates_list = []
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
            MEI_instructions = TransformData(
                    arranger_to_editor=arranger_to_editor,
                    obliterate_incipit=obliterate_incipit,
                    replace_longa=replace_longa,
                    editorial_resp=editorial_resp,
                    alternates_list=alternates_list,
                    color_for_ficta=color_for_ficta,
                )
            write_transformation(str(MEI_filename), MEI_instructions)

    # Handle file upload
    if request.method == 'POST':
        if request.POST.get('action') == 'Delete':
            MEI_filename = request.POST.get('selection')
            doc_set = Document.objects.filter(docfile=MEI_filename)
            if len(doc_set)>0:
                default_storage.delete(MEI_filename)
                doc_set[0].delete()
        elif request.POST.get('action') == 'Process':
                process(request)

    form = DocumentForm() # A empty, unbound form
    items = Document.objects.all() # Load documents for the list page

    # Render list page with the documents and the form
    return render_to_response('frontEnd/list.html',
                              {'items': items, 'form': form},
        context_instance=RequestContext(request)
    )

def metadata(request):
    if request.method == 'POST':
        # str() converts from unicode to str
        newdoc = Document(docfile = request.FILES['plainmei'])
        newdoc.save()
        MEI_filename = newdoc.docfile.path
        analysis = make_analysis(str(MEI_filename))
        # "variant" or "reconstruction" or "concordance"
        processType = request.POST.get('processType')
    else:
        html = "<html><body>No file selected</body></html>"
        return HttpResponse(html)

    return render_to_response('frontEnd/metadata.html',
            {'MEI_filename': MEI_filename,
                    'has_editor_element': analysis.has_editor_element,
                    'has_arranger_element': analysis.has_arranger_element,
                    'editor_name': analysis.editor_name,
                    'staff_list': analysis.staff_list
            },
            context_instance=RequestContext(request))
