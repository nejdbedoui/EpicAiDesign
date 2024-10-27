from django import forms
from TagsVideoApp.models import Tag

class VideoForm(forms.Form):
    name = forms.CharField(max_length=255, label="Nom de la vidéo")
    prompt = forms.CharField(widget=forms.Textarea, label="Description utilisée pour générer la vidéo")
    display = forms.BooleanField(required=False, initial=True, label="Afficher la vidéo")
    tags = forms.MultipleChoiceField(
        choices=[(str(tag.id), tag.name) for tag in Tag.objects.all()],
        widget=forms.SelectMultiple(),
        required=False,
        label="Select tags"
    )

class UpdateVideoForm(forms.Form):
    name = forms.CharField(max_length=255, label="Nom de la vidéo")
    display = forms.BooleanField(required=False, label="Afficher la vidéo")
    tags = forms.MultipleChoiceField(
        choices=[(str(tag.id), tag.name) for tag in Tag.objects],  # Générer les choix
        widget=forms.SelectMultiple(),
        required=False,
        label="Select tags"
    )

class TagForm(forms.Form):
    name = forms.CharField(max_length=255, label="Nom de la tag")