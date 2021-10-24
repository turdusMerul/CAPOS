import os
import re
from docx import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import AudioForm
from .models import Audio
from .transcriber import transcribe


def index(request):
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            file = Audio(audiofile=request.FILES['audiofile'])
            file_name = str(file)
            file.save()
            text = transcribe(str(file))
            os.remove(str(f"{settings.MEDIA_ROOT}/{file}"))
            doc = Document()
            doc.add_paragraph(text.lower())
            file.delete()
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={file_name}_transcribed.docx'
            doc.save(response)

            return response
    else:
        form = AudioForm()
    return render(request, 'main/index.html', {'form': form})

def changes(request):
    return render(request, 'main/changes.html')

def contacts(request):
    return render(request, 'main/contacts.html')