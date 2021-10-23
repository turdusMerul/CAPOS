from django import forms
from django.forms import ModelForm, FileInput
from .models import Audio


class AudioForm(ModelForm):
    class Meta:
        model = Audio
        fields = ["audiofile"] 
        widgets = {
            "audiofile" : FileInput(attrs={
                "accept" : ".wav"
            })
        }