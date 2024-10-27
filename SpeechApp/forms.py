from django import forms

class SpeechForm(forms.Form):
    name = forms.CharField(max_length=255, label="Nom de speech")
    text = forms.CharField(widget=forms.Textarea, label="Description utilisée pour générer le speech")
    display = forms.BooleanField(required=False, initial=True, label="Afficher le speech")

class UpdateSpeechForm(forms.Form):
    name = forms.CharField(max_length=255, label="Nom de speech")
    display = forms.BooleanField(required=False, label="Afficher le speech")