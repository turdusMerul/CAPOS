from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('changes', views.changes, name='changes'),
    path('contacts', views.contacts, name='contacts')
]
