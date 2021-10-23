import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import AudioForm
from .models import Audio
from .transcriber import transcribe


def index(request):
    if request.method == "POST":
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            file = Audio(audiofile=request.FILES['audiofile'])
            file.save()
            print(transcribe(str(file)))
            os.remove(str(file))
            file.delete()
            return HttpResponseRedirect('/')
    else:
        form = AudioForm()
    return render(request, 'main/index.html', {'form': form})

def changes(request):
    return render(request, 'main/changes.html')

def contacts(request):
    return render(request, 'main/contacts.html')