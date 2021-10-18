from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h4>Welcome to the main page of CAPOS!</h4>')