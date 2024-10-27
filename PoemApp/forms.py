from django import forms
from .models import PoemArt

class PoemForm(forms.Form):  # Utilisation de forms.Form au lieu de forms.ModelForm
    title = forms.CharField(max_length=200, label='Title')
    category = forms.CharField(max_length=100, label='Category')
    text = forms.CharField(widget=forms.Textarea, label='Text')
    public = forms.BooleanField(required=False, label='Public')  # Champs pour le statut public
    rating = forms.FloatField(required=False, label='Rating')  # Champs pour la note
