from django import forms

class IdeaForm(forms.Form):
    title = forms.CharField(label="Ttitle", max_length=50, required=True)
    text = forms.CharField(label="Text", required=True)