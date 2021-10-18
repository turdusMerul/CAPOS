from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def signIn(request):
    return render(request, 'main/signIn.html')