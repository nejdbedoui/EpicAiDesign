from django import forms

class TagForm(forms.ModelForm):
    name = forms.CharField(max_length=255, label="Nom de la tag")